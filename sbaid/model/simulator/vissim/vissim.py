"""
The module containing the vissim connector that talks to vissim via COM.
It exposes the VissimConnector class that exposes async methods to interact
with vissim.
"""

import threading
from threading import Thread
import asyncio
import bisect
from queue import Queue
from typing import Any, NamedTuple, Callable, cast

# pylint: disable=import-error
import pythoncom  # type: ignore
# pylint: disable=import-error
import win32com.client as com  # type: ignore

from gi.repository import GLib, Gio

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.input import Input
from sbaid.model.simulator.vissim.vissim_network import VissimNetwork, InvalidLocationException


class VissimNotFoundException(Exception):
    """Raised if starting vissim via com fails."""


class _VissimCommand:
    future: asyncio.Future[Any]

    def __init__(self, func: Callable[..., Any] | None, *args: Any) -> None:
        self.future = asyncio.get_event_loop().create_future()
        self.func = func
        self.args = args

    def run(self) -> bool:
        """
        Runs the func given in the constructor. Should be called in the worker thread.
        As it will schedule a threadsafe call back on the future with the results from
        running the func. Returns true if the worker thread should continue, false otherwise.
        """
        if self.func:
            try:
                results = self.func(*self.args)
                self.future.get_loop().call_soon_threadsafe(self.future.set_result, results)
            except Exception as e:  # pylint: disable=broad-exception-caught
                self.future.get_loop().call_soon_threadsafe(self.future.set_exception, e)

            GLib.idle_add(lambda: GLib.SOURCE_REMOVE)  # Make sure we get a loop iteration
            return True

        self.future.get_loop().call_soon_threadsafe(self.future.set_result, None)
        GLib.idle_add(lambda: GLib.SOURCE_REMOVE)  # Make sure we get a loop iteration
        return False


class VissimConnectorCrossSectionState(NamedTuple):
    """
    The current state of a cross section in vissim. Immutable once created and only used
    to transfer the information between threads.
    """
    id: str
    name: str
    type: CrossSectionType
    location: Location
    lanes: int
    successors: list[str]


class _CrossSection:
    __network: VissimNetwork

    __data_collection_points: list[Any]
    __des_speed_decisions: list[Any]

    __current_a_display: dict[int, ADisplay]
    __current_b_display: BDisplay

    @property
    def successors(self) -> list[str]:
        """
        Returns the ids of the cross sections that are direct successors to this cross section.
        """
        return self.__network.get_cross_section_successors(self.link_no, self.link_pos)

    @property
    def link_no(self) -> int:
        """Returns the unique vissim number of the link on which this cross section is located."""
        if self.__data_collection_points:
            return cast(int, self.__data_collection_points[0].Lane.Link.AttValue("No"))
        return cast(int, self.__des_speed_decisions[0].Lane.Link.AttValue("No"))

    @property
    def link_pos(self) -> float:
        """Returns the position on the link at which this cross section is located."""
        if self.__data_collection_points:
            return cast(float, self.__data_collection_points[0].AttValue("Pos"))
        return cast(float, self.__des_speed_decisions[0].AttValue("Pos"))

    @property
    def primary_point_id(self) -> int:
        """
        Returns the unique number provided by vissim of the primary point that make up this cross
        section. The primary point is the data collection point on lane 0 (or 1 in vissim terms)
        if the cross section has measuring capabilities and the desired speed decision
        on lane 0 (or 1 in vissim terms) if it doesn't.
        """
        if self.__data_collection_points:
            return cast(int, self.__data_collection_points[0].AttValue("No"))

        return cast(int, self.__des_speed_decisions[0].AttValue("No"))

    @property
    def id(self) -> str:
        """Returns the unique id of the cross section."""
        return str(self.primary_point_id)

    @property
    def name(self) -> str:
        """Returns the name of the cross section. Made up of names of the individual points."""
        name = ""
        for point in self.__data_collection_points:
            name += point.AttValue("Name")

        for decision in self.__des_speed_decisions:
            name += decision.AttValue("Name")

        return name

    @property
    def type(self) -> CrossSectionType:
        """Returns the type of the cross section."""
        if not self.__des_speed_decisions:
            return CrossSectionType.MEASURING

        if not self.__data_collection_points:
            return CrossSectionType.DISPLAY

        return CrossSectionType.COMBINED

    @property
    def location(self) -> Location:
        """Returns the location of the cross section."""
        if self.__data_collection_points:
            middle = int(len(self.__data_collection_points) / 2)
            x = self.__data_collection_points[middle].AttValue("LongWGS84")
            y = self.__data_collection_points[middle].AttValue("LatWGS84")
            return Location(x, y)

        middle = int(len(self.__des_speed_decisions) / 2)
        x = self.__des_speed_decisions[middle].AttValue("LongWGS84")
        y = self.__des_speed_decisions[middle].AttValue("LatWGS84")
        return Location(x, y)

    @property
    def lanes(self) -> int:
        """Returns the number of lanes at this cross section."""
        if self.__data_collection_points:
            return len(self.__data_collection_points)

        return len(self.__des_speed_decisions)

    @property
    def data_collection_points(self) -> list[Any]:
        """
        Returns a list of data collection points that are used for the measuring capabilities
        of this cross section.
        """
        return self.__data_collection_points.copy()

    @property
    def des_speed_decisions(self) -> list[Any]:
        """
        Returns a list of desired speed decisions that are used for the display cross
        section capabilities.
        """
        return self.__des_speed_decisions.copy()

    @property
    def state(self) -> VissimConnectorCrossSectionState:
        """Returns the current state of this cross section."""
        return VissimConnectorCrossSectionState(self.id, self.name, self.type, self.location,
                                                self.lanes, self.successors)

    def __init__(self, network: VissimNetwork) -> None:
        self.__network = network

        self.__data_collection_points = []
        self.__des_speed_decisions = []

        self.__current_a_display = {}
        self.__current_b_display = BDisplay.OFF

    def add_data_collection_point(self, point: Any) -> None:
        """Adds the given data collection point to this cross section."""
        bisect.insort(self.__data_collection_points, point,
                      key=lambda x: x.Lane.AttValue("Index"))

    def add_des_speed_decision(self, des_speed_decision: Any) -> None:
        """Adds the given desired speed decision to this cross section."""
        bisect.insort(self.__des_speed_decisions, des_speed_decision,
                      key=lambda x: x.Lane.AttValue("Index"))

    def remove_data_collection_point(self, point: Any) -> None:
        """Removes the given data collection point from this cross section."""
        self.__data_collection_points.remove(point)

    def remove_des_speed_decision(self, des_speed_decision: Any) -> None:
        """Removes the given desired speed decision from this cross section."""
        self.__des_speed_decisions.remove(des_speed_decision)

    def measure(self, algo_input: Input) -> None:
        """
        Fills the given Input with measurements at this cross section from the last
        evaluation interval.
        """
        if not self.__data_collection_points:
            return

        for lane_index, point in enumerate(self.__data_collection_points, 1):
            for measurement in point.DataCollMeas.GetAll():
                avg_speed = measurement.AttValue("SpeedAvgArith(Current,Last,All)")
                traffic_volume = measurement.AttValue("Vehs(Current,Last,All)")
                algo_input.add_lane_info(self.id, lane_index, avg_speed, traffic_volume)

    def set_display(self, display: Display, distr_by_speed: dict[int, int]) -> None:
        """
        Sets the given display at this cross section.
        :param display: information about the signs that should be displayed
        :param distr_by_speed: the ids of the desired speed distribution for a given speed limit
        """
        if not self.__des_speed_decisions:
            return

        b_display = display.get_b_display(self.id)

        display_changed = self.__current_b_display != b_display
        for lane_index in range(1, self.lanes + 1):
            if display_changed:
                break

            display_changed = (self.__current_a_display.get(lane_index) !=
                               display.get_a_display(self.id, lane_index - 1))

        if not display_changed:
            return

        blocked_classes_by_lane = {}

        self.__current_b_display = b_display

        lorry_no_overtaking = b_display == BDisplay.LORRY_NO_OVERTAKING

        found_open_lane = False
        for lane_index, decision in enumerate(self.__des_speed_decisions, 1):
            a_display = display.get_a_display(self.id, lane_index - 1)

            self.__current_a_display[lane_index] = a_display

            speed, closed = self.__get_lane_config(a_display)

            distr = distr_by_speed[speed]
            # Set the speed for all vehicle types
            decision.SetAttValue("DesSpeedDistr(10)", distr)
            decision.SetAttValue("DesSpeedDistr(11)", distr)
            decision.SetAttValue("DesSpeedDistr(20)", distr)
            decision.SetAttValue("DesSpeedDistr(21)", distr)
            decision.SetAttValue("DesSpeedDistr(30)", distr)

            if closed:
                blocked_classes_by_lane[lane_index] = "10, 11, 20, 21, 30"
            elif found_open_lane and lorry_no_overtaking:  # We need at least one open lane
                blocked_classes_by_lane[lane_index] = "20, 21, 30"
            else:
                found_open_lane = True
                blocked_classes_by_lane[lane_index] = ""

        for link in self.__network.get_cross_section_links(self.link_no, self.link_pos):
            self.__configure_blocked_lanes(link, blocked_classes_by_lane)

    def __get_lane_config(self, a_display: ADisplay) -> tuple[int, bool]:
        speed = 130
        match a_display:
            case ADisplay.SPEED_LIMIT_60:
                speed = 60
            case ADisplay.SPEED_LIMIT_80:
                speed = 80
            case ADisplay.SPEED_LIMIT_100:
                speed = 100
            case ADisplay.SPEED_LIMIT_110:
                speed = 110
            case ADisplay.SPEED_LIMIT_120:
                speed = 120
            case ADisplay.SPEED_LIMIT_130:
                speed = 130

        return speed, a_display == ADisplay.CLOSED_LANE

    def __configure_blocked_lanes(self, link: Any, blocked_classes_by_lane: dict[int, str]) -> None:
        for i, lane in enumerate(link.Lanes.GetAll(), 1):
            blocked_ch_r = blocked_classes_by_lane.get(i - 1) or ""
            blocked = blocked_classes_by_lane.get(i) or ""
            blocked_ch_l = blocked_classes_by_lane.get(i + 1) or ""
            lane.SetAttValue("NoLnChRVehClasses", blocked_ch_r)
            lane.SetAttValue("BlockedVehClasses", blocked)
            lane.SetAttValue("NoLnChLVehClasses", blocked_ch_l)


class VissimConnector:
    """
    The main class for interacting with vissim. It starts a new thread and handles all interactions
    with vissim in that thread. This is to allow the main thread to continue running while
   lengthy operations are occasionally performed with Vissim. Since COM doesn't play nicely with
    multiple thread we have to keep all COM communication and objects in that thread.
    """
    __thread: Thread
    __queue: Queue[_VissimCommand]
    __vissim: Any = None  # For the COM interface we use dynamic typing
    __network: VissimNetwork
    __cross_sections_by_id: dict[str, _CrossSection]
    __speed_distr_by_speed: dict[int, int]

    def __init__(self) -> None:
        self.__queue = Queue()
        self.__thread = Thread(target=self.__thread_func, args=(self.__queue,), daemon=True)
        self.__thread.start()

        app = Gio.Application.get_default()  # pylint: disable=no-value-for-parameter
        if app:
            app.connect("shutdown", self.__on_app_shutdown)

    async def __push_command(self, func: Callable[..., Any] | None, *args: Any) -> Any:
        command = _VissimCommand(func, *args)
        self.__queue.put(command)
        return await command.future

    def __thread_func(self, queue: Queue[_VissimCommand]) -> None:
        assert threading.current_thread() == self.__thread

        pythoncom.CoInitialize()

        while queue.get().run():
            pass

        if self.__vissim:
            self.__vissim.Exit()
            self.__vissim = None
        pythoncom.CoUninitialize()

    async def load_file(self,
                        path: str) -> tuple[list[Location], list[VissimConnectorCrossSectionState]]:
        """
        Loads the .inpx file with the given path into vissim.
        :param path: the path of the .inpx file to load
        :return: the list of location that make up the main route and a list of cross section states
        of cross sections that are on the route
        """
        result = await self.__push_command(self.__load_file, path)
        return cast(tuple[list[Location], list[VissimConnectorCrossSectionState]], result)

    def __load_file(self,
                    path: str) -> tuple[list[Location], list[VissimConnectorCrossSectionState]]:
        assert threading.current_thread() == self.__thread

        self.__cross_sections_by_id = {}

        try:
            self.__vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
        except Exception as e:
            raise VissimNotFoundException(e) from e

        self.__vissim.LoadNet(path, False)
        self.__network = VissimNetwork(self.__vissim.Net)

        self.__init_speed_distributions()

        cs_by_link_and_pos = self.__get_cross_sections_by_link_and_pos()

        for link_no, cs_by_pos in cs_by_link_and_pos.items():
            for pos, cs in cs_by_pos.items():
                self.__cross_sections_by_id[cs.id] = cs
                self.__network.add_cross_section(link_no, pos, cs.id)

        route, cross_section_ids = self.__network.get_main_route()

        for cs_id in list(self.__cross_sections_by_id.keys()):
            if cs_id not in cross_section_ids:
                self.__cross_sections_by_id.pop(cs_id)

        return route, list(map(lambda x: self.__cross_sections_by_id[x].state, cross_section_ids))

    def __init_speed_distributions(self) -> None:
        distr_60 = [50.0, 0.0, 60.0, 1.0]
        distr_80 = [70.0, 0.0, 80.0, 1.0]
        distr_100 = [80.0, 0.0, 100.0, 1.0]
        distr_110 = [90.0, 0.0, 110.0, 1.0]
        distr_120 = [100.0, 0.0, 120.0, 1.0]
        distr_130 = [100.0, 0.0, 130.0, 1.0]

        self.__speed_distr_by_speed = {60: self.__add_speed_distribution(distr_60),
                                       80: self.__add_speed_distribution(distr_80),
                                       100: self.__add_speed_distribution(distr_100),
                                       110: self.__add_speed_distribution(distr_110),
                                       120: self.__add_speed_distribution(distr_120),
                                       130: self.__add_speed_distribution(distr_130)}

    def __add_speed_distribution(self, points: list[float]) -> int:
        distr = self.__vissim.Net.DesSpeedDistributions.AddDesSpeedDistribution(None, points)
        return cast(int, distr.AttValue("No"))

    def __get_cross_sections_by_link_and_pos(self) -> dict[int, dict[float, _CrossSection]]:
        cs_by_link_and_pos: dict[int, dict[float, _CrossSection]] = {}

        points = self.__vissim.Net.DataCollectionPoints.GetAll()
        for point in points:
            link_no = point.Lane.Link.AttValue("No")
            pos = point.AttValue("Pos")

            if link_no not in cs_by_link_and_pos:
                cs_by_link_and_pos[link_no] = {}

            if pos not in cs_by_link_and_pos[link_no]:
                cs_by_link_and_pos[link_no][pos] = _CrossSection(self.__network)

            cs_by_link_and_pos[link_no][pos].add_data_collection_point(point)

        decisions = self.__vissim.Net.DesSpeedDecisions.GetAll()
        for dec in decisions:
            link_no = dec.Lane.Link.AttValue("No")
            pos = dec.AttValue("Pos")

            if link_no not in cs_by_link_and_pos:
                cs_by_link_and_pos[link_no] = {}
            # Adjust pos to merge with a measuring cross section if close enough
            elif pos not in cs_by_link_and_pos:
                existing_cs = cs_by_link_and_pos[link_no].values()
                for cs in existing_cs:
                    if abs(pos - cs.link_pos) <= 5:
                        pos = cs.link_pos

            if pos not in cs_by_link_and_pos[link_no]:
                cs_by_link_and_pos[link_no][pos] = _CrossSection(self.__network)

            cs_by_link_and_pos[link_no][pos].add_des_speed_decision(dec)

        return cs_by_link_and_pos

    async def create_cross_section(self, location: Location,
                                   cs_type: CrossSectionType) -> VissimConnectorCrossSectionState:
        """
        Creates a new cross section in vissim.
        :param location: the location at which to add the new cross section
        :param cs_type: the type of the new cross section
        :return: the state of the newly created cross section
        """
        result = await self.__push_command(self.__create_cross_section, location, cs_type)
        return cast(VissimConnectorCrossSectionState, result)

    def __create_cross_section(self, location: Location,
                               cs_type: CrossSectionType) -> VissimConnectorCrossSectionState:
        assert threading.current_thread() == self.__thread

        cross_section = _CrossSection(self.__network)

        self.__add_cs_to_vissim(cross_section, location, cs_type)

        self.__cross_sections_by_id[cross_section.id] = cross_section

        self.__vissim.SaveNet()

        return cross_section.state

    async def remove_cross_section(self, cs_id: str) -> None:
        """
        Removes a cross section from vissim.
        :param cs_id: the id of the cross section to remove
        """
        await self.__push_command(self.__remove_cross_section, cs_id)

    def __remove_cross_section(self, cs_id: str) -> None:
        assert threading.current_thread() == self.__thread

        cross_section = self.__cross_sections_by_id.pop(cs_id)
        self.__remove_cs_from_vissim(cross_section)

        self.__vissim.SaveNet()

    async def move_cross_section(self, cs_id: str,
                                 new_location: Location) -> VissimConnectorCrossSectionState:
        """
        Moves a cross section to a new location in vissim.
        :param cs_id: the id of the cross section to move
        :param new_location: the new location to which the cross section should be moved
        :return: the new state of the cross section
        """
        result = await self.__push_command(self.__move_cross_section, cs_id, new_location)
        return cast(VissimConnectorCrossSectionState, result)

    def __move_cross_section(self, cs_id: str,
                             new_location: Location) -> VissimConnectorCrossSectionState:
        assert threading.current_thread() == self.__thread

        if not self.__network.contains_point(new_location):
            raise InvalidLocationException("The given location is not in the network.")

        cross_section = self.__cross_sections_by_id[cs_id]

        # The properties are calculated automatically through the data points, so cache them
        # because deletion will delete the points and therefore reset the properties
        cs_type = cross_section.type
        primary_point_id = cross_section.primary_point_id

        self.__remove_cs_from_vissim(cross_section)
        self.__add_cs_to_vissim(cross_section, new_location, cs_type, primary_point_id)

        # If this doesn't hold we get a bunch of problems so better assert it
        assert cross_section.id == cs_id

        self.__vissim.SaveNet()

        return cross_section.state

    def __add_cs_to_vissim(self, cross_section: _CrossSection, location: Location,
                           cs_type: CrossSectionType, first_id: int | None = None) -> None:
        assert threading.current_thread() == self.__thread

        link, pos = self.__network.get_link_and_position(location)

        data_collection_points = self.__vissim.Net.DataCollectionPoints
        des_speed_decisions = self.__vissim.Net.DesSpeedDecisions

        for lane in link.Lanes.GetAll():
            if cs_type in (CrossSectionType.MEASURING, CrossSectionType.COMBINED):
                point = data_collection_points.AddDataCollectionPoint(first_id, lane, pos)
                first_id = None
                cross_section.add_data_collection_point(point)

            if cs_type in (CrossSectionType.DISPLAY, CrossSectionType.COMBINED):
                decision = des_speed_decisions.AddDesSpeedDecision(first_id, lane, pos)
                first_id = None
                cross_section.add_des_speed_decision(decision)

        self.__network.add_cross_section(cross_section.link_no, cross_section.link_pos,
                                         cross_section.id)

    def __remove_cs_from_vissim(self, cross_section: _CrossSection) -> None:
        assert threading.current_thread() == self.__thread

        self.__network.remove_cross_section(cross_section.link_no, cross_section.link_pos)

        point_container = self.__vissim.Net.DataCollectionPoints

        for point in cross_section.data_collection_points:
            point_container.RemoveDataCollectionPoint(point)
            cross_section.remove_data_collection_point(point)

        decision_container = self.__vissim.Net.DesSpeedDecisions

        for decision in cross_section.des_speed_decisions:
            decision_container.RemoveDesSpeedDecision(decision)
            cross_section.remove_des_speed_decision(decision)

    async def init_simulation(self, eval_interval: int) -> tuple[GLib.DateTime, int]:
        """
        Initializes the simulation in vissim.
        :param eval_interval: the interval in seconds at which new measurements should be taken
        at the cross sections
        :return: the in simulation time and date at which the simulation starts and the number of
        seconds for which the simulation runs
        """
        result = await self.__push_command(self.__init_simulation, eval_interval)
        return cast(tuple[GLib.DateTime, int], result)

    def __init_simulation(self, eval_interval: int) -> tuple[GLib.DateTime, int]:
        assert threading.current_thread() == self.__thread

        sim_start = self.__vissim.Simulation.AttValue('StartTm')

        sim_start_time = GLib.DateTime.new_utc(1, 1, 1, 0, 0, 0)

        if sim_start_time is None:
            assert False

        sim_start_time = sim_start_time.add_seconds(sim_start)

        sim_duration = self.__vissim.Simulation.AttValue('SimPeriod')

        self.__vissim.Net.Evaluation.SetAttValue("DataCollCollectData", 1)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollInterval", eval_interval)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollFromTime", 0)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollToTime", sim_duration)

        self.__vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
        self.__vissim.Simulation.SetAttValue('SimBreakAt', 0)
        self.__vissim.Simulation.RunSingleStep()  # Actually starts the simulation
        return sim_start_time, sim_duration

    async def continue_simulation(self, span: int) -> None:
        """
        Continues the simulation for the given span.
        :param span: the timespan of seconds to simulate
        """
        await self.__push_command(self.__continue_simulation, span)

    def __continue_simulation(self, span: int) -> None:
        assert threading.current_thread() == self.__thread

        current_break = self.__vissim.Simulation.AttValue('SimBreakAt')
        self.__vissim.Simulation.SetAttValue('SimBreakAt', current_break + span)
        self.__vissim.Simulation.RunContinuous()

    async def measure(self) -> Input:
        """
        Takes measurements at the cross sections and returns them.
        :return: an Input containing measurements from the cross sections
        """
        return cast(Input, await self.__push_command(self.__measure))

    def __measure(self) -> Input:
        assert threading.current_thread() == self.__thread

        algo_input = Input()
        for cross_section in self.__cross_sections_by_id.values():
            cross_section.measure(algo_input)

        return algo_input

    async def set_display(self, display: Display) -> None:
        """
        Sets the display for the cross sections.
        :param display: information about the signs to display at the cross sections
        """
        await self.__push_command(self.__set_display, display)

    def __set_display(self, display: Display) -> None:
        assert threading.current_thread() == self.__thread

        for cross_section in self.__cross_sections_by_id.values():
            cross_section.set_display(display, self.__speed_distr_by_speed)

    async def stop_simulation(self) -> None:
        """
        Stops the simulation.
        """
        await self.__push_command(self.__stop_simulation)

    def __stop_simulation(self) -> None:
        assert threading.current_thread() == self.__thread

        self.__vissim.Simulation.Stop()

    async def shutdown(self) -> None:
        """
        Shuts down the simulator, freeing all resources in the process.
        """
        await self.__push_command(None)

    def __on_app_shutdown(self, app: Gio.Application) -> None:
        self.__queue.put(_VissimCommand(None))
        self.__thread.join()
