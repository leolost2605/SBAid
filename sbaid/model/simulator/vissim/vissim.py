"""TODO"""
import threading

import win32com.client as com
import asyncio
import pythoncom
from queue import Queue
from typing import Any, NamedTuple, Callable
from threading import Thread

from sbaid.common.a_display import ADisplay
from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.input import Input
from sbaid.model.simulator.vissim.vissim_network import VissimNetwork


class VissimNotFoundException(Exception):
    pass


class VissimCommand:
    future: asyncio.Future[Any]

    def __init__(self, func: Callable[..., ...] | None, *args: Any) -> None:
        self.future = asyncio.get_event_loop().create_future()
        self.func = func
        self.args = args

    def run(self) -> bool:
        if self.func:
            results = self.func(*self.args)
        else:
            results = None

        self.future.get_loop().call_soon_threadsafe(self.future.set_result, results)

        return self.func is not None


class VissimConnectorCrossSectionState(NamedTuple):
    id: str
    type: CrossSectionType
    position: Coordinate
    lanes: int
    successors: list[str]


class _CrossSection:
    __cs_by_link_and_pos: dict[int, dict[float, '_CrossSection']]
    __network: VissimNetwork

    __successors: list[tuple[int, '_CrossSection']]

    __data_collection_points: list[Any]
    __des_speed_decisions: list[Any]

    @property
    def link_index(self) -> int:
        if self.__data_collection_points:
            return self.__data_collection_points[0].Lane.Link.AttValue("No")
        return self.__des_speed_decisions[0].Lane.Link.AttValue("No")

    @property
    def pos_on_link(self) -> float:
        if self.__data_collection_points:
            return self.__data_collection_points[0].AttValue("Pos")
        return self.__des_speed_decisions[0].AttValue("Pos")

    @property
    def primary_point_id(self) -> int:
        if self.__data_collection_points:
            return self.__data_collection_points[0].AttValue("No")

        return self.__des_speed_decisions[0].AttValue("No")

    @property
    def id(self):
        return str(self.primary_point_id)

    @property
    def type(self) -> CrossSectionType:
        if not self.__des_speed_decisions:
            return CrossSectionType.MEASURING

        if not self.__data_collection_points:
            return CrossSectionType.DISPLAY

        return CrossSectionType.COMBINED

    @property
    def position(self) -> Coordinate:
        return None

    @property
    def lanes(self) -> int:
        if self.__data_collection_points:
            return len(self.__data_collection_points)

        return len(self.__des_speed_decisions)

    @property
    def data_collection_points(self) -> list[Any]:
        return self.__data_collection_points.copy()

    @property
    def des_speed_decisions(self) -> list[Any]:
        return self.__des_speed_decisions.copy()

    def __init__(self, cs_by_link_and_pos: dict[int, dict[float, '_CrossSection']],
                 network: VissimNetwork) -> None:
        self.__cs_by_link_and_pos = cs_by_link_and_pos
        self.__network = network

        self.__successors = []

        self.__data_collection_points = []
        self.__des_speed_decisions = []

    def add_data_collection_point(self, point: Any) -> None:
        self.__data_collection_points.append(point)

    def add_des_speed_decision(self, des_speed_decision: Any) -> None:
        self.__des_speed_decisions.append(des_speed_decision)

    def remove_data_collection_point(self, point: Any) -> None:
        self.__data_collection_points.remove(point)

    def remove_des_speed_decision(self, des_speed_decision: Any) -> None:
        self.__des_speed_decisions.remove(des_speed_decision)

    def update_successors(self) -> None:
        """Walks the network and adds the first cross section on every possible route as successor"""
        self.__successors.clear()

        if self.__data_collection_points:
            link_no = self.__data_collection_points[0].Lane.Link.AttValue("No")
        else:
            link_no = self.__des_speed_decisions[0].Lane.Link.AttValue("No")

        self.__walk_link(link_no, set())

    def __walk_link(self, link_no: int, walked: set[int]) -> None:
        if link_no in walked:  # Protect against cycles
            return

        walked.add(link_no)

        if self.__add_successor(link_no):
            return

        for successor in self.__network.get_successors(link_no):
            self.__walk_link(successor, walked)

    def __add_successor(self, link_no: int) -> bool:
        if link_no not in self.__cs_by_link_and_pos:
            return False

        sorted_pos = list(self.__cs_by_link_and_pos[link_no].keys())
        sorted_pos.sort()
        for pos in sorted_pos:
            if (cs := self.__cs_by_link_and_pos[link_no][pos]) != self:  # TODO: doesn't check for earlier ones
                self.__successors.append((0, cs))
                return True

        return False

    # def add_to_vissim(self, position: Coordinate, cs_type: CrossSectionType) -> None:
    #     self.__add_to_vissim(position, cs_type, None)
    #     self.__update_all_successors()
    #
    # def remove_from_vissim(self) -> None:
    #     self.__remove_from_vissim()
    #     self.__update_all_successors()
    #
    # def move_in_vissim(self, new_position: Coordinate) -> None:
    #     # The properties are calculated automatically through the data points, so cache them
    #     # because deletion will delete the points and therefore reset the properties
    #     old_id = self.id
    #     cs_type = self.type
    #     primary_point_id = self.primary_point_id
    #
    #     self.__remove_from_vissim()
    #     self.__add_to_vissim(new_position, cs_type, primary_point_id)
    #
    #     assert self.id == old_id  # If this doesn't hold we get a bunch of problems so better assert it
    #
    #     self.__update_all_successors()
    #
    # def __add_to_vissim(self, position: Coordinate, cs_type: CrossSectionType, first_id: int | None) -> None:
    #     link, pos = self.__network.get_link_and_position(position)
    #
    #     link_no = link.AttValue("No")
    #
    #     if link_no not in self.__cs_by_link_and_pos:
    #         self.__cs_by_link_and_pos[link_no] = {}
    #
    #     # If this doesn't hold we currently get problems, so assert it for now but maybe TODO conflict detection
    #     assert pos not in self.__cs_by_link_and_pos[link_no]
    #
    #     self.__cs_by_link_and_pos[link_no][pos] = self
    #
    #     data_collection_points = self.__vissim.Net.DataCollectionPoints
    #     des_speed_decisions = self.__vissim.Net.DesSpeedDecisions
    #
    #     for lane in link.Lanes.GetAll():
    #         if cs_type == CrossSectionType.MEASURING or cs_type == CrossSectionType.COMBINED:
    #             point = data_collection_points.AddDataCollectionPoint(first_id, lane, pos)
    #             first_id = None
    #             self.__data_collection_points.append(point)
    #
    #         if cs_type == CrossSectionType.DISPLAY or cs_type == CrossSectionType.COMBINED:
    #             decision = des_speed_decisions.AddDesSpeedDecision(first_id, lane, pos)
    #             first_id = None
    #             self.__des_speed_decisions.append(decision)
    #
    # def __remove_from_vissim(self) -> None:
    #     self.__cs_by_link_and_pos[self.link_index].pop(self.pos_on_link)
    #
    #     if not self.__cs_by_link_and_pos[self.link_index]:
    #         self.__cs_by_link_and_pos.pop(self.link_index)
    #
    #     point_container = self.__vissim.Net.DataCollectionPoints
    #
    #     for point in self.__data_collection_points:
    #         point_container.RemoveDataCollectionPoint(point)
    #
    #     self.__data_collection_points.clear()
    #
    #     decision_container = self.__vissim.Net.DesSpeedDecisions
    #
    #     for decision in self.__des_speed_decisions:
    #         decision_container.RemoveDesSpeedDecision(decision)
    #
    #     self.__des_speed_decisions.clear()

    def get_state(self) -> VissimConnectorCrossSectionState:
        successor_ids = list(map(lambda cs: cs[1].id, self.__successors))
        return VissimConnectorCrossSectionState(self.id, self.type, self.position, self.lanes, successor_ids)

    def measure(self, algo_input: Input) -> None:
        for i, point in enumerate(self.__data_collection_points):
            lane_index = point.Lane.AttValue("Index") - 1
            for measurement in point.DataCollMeas.GetAll():
                avg_speed = measurement.AttValue("SpeedAvgArith(Current,Last,All)")
                print(f"avg speed for {self.id} on lane {lane_index}: {avg_speed}")

    def set_display(self, display: Display) -> None:
        if not self.__des_speed_decisions:
            return

        for decision in self.__des_speed_decisions:
            lane_index = decision.Lane.AttValue("Index") - 1
            a_display = display.get_a_display(self.id, lane_index)
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

            decision.SetAttValue("DesSpeedDistr(All)", speed)

            blocked = "10, 11, 20, 21, 30" if a_display == ADisplay.CLOSED_LANE else ""
            decision.Lane.SetAttValue("BlockedVehClasses", blocked)
            # Maybe TODO: neighbor_lane.SetAttValue("NoLnChRAllVehTypes", True)


class VissimConnector:
    __thread: Thread
    __queue: Queue[VissimCommand]
    __vissim: Any  # For the COM interface we use dynamic typing
    __network: VissimNetwork | None
    __cs_by_link_and_pos: dict[int, dict[float, _CrossSection]]
    __cross_sections_by_id: dict[str, _CrossSection]

    def __init__(self) -> None:
        self.__queue = Queue()
        self.__thread = Thread(target=self.__thread_func, args=(self.__queue,), daemon=True)
        self.__thread.start()

    async def __push_command(self, func: Callable[..., ...] | None, *args: Any) -> Any:
        command = VissimCommand(func, *args)
        self.__queue.put(command)
        return await command.future

    def __thread_func(self, queue: Queue[VissimCommand]) -> None:
        assert threading.current_thread() == self.__thread

        pythoncom.CoInitialize()

        while queue.get().run():
            pass

        self.__vissim.Exit()
        self.__vissim = None
        self.__network = None
        pythoncom.CoUninitialize()

    def __update_all_successors(self) -> None:
        assert threading.current_thread() == self.__thread

        for cs in self.__cross_sections_by_id.values():
            cs.update_successors()

    async def load_file(self, path: str) -> tuple[list[Coordinate], list[VissimConnectorCrossSectionState]]:
        return await self.__push_command(self.__load_file, path)

    def __load_file(self, path: str) -> tuple[list[Coordinate], list[VissimConnectorCrossSectionState]]:
        assert threading.current_thread() == self.__thread

        self.__cs_by_link_and_pos = {}
        self.__cross_sections_by_id = {}

        try:
            self.__vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
        except Exception as e:
            raise VissimNotFoundException(e)

        self.__vissim.LoadNet(path, False)
        self.__network = VissimNetwork(self.__vissim.Net)

        print("Network created")

        points = self.__vissim.Net.DataCollectionPoints.GetAll()

        for point in points:
            link_index = point.Lane.Link.AttValue("No")
            pos = point.AttValue("Pos")

            if link_index not in self.__cs_by_link_and_pos:
                self.__cs_by_link_and_pos[link_index] = {}

            if pos not in self.__cs_by_link_and_pos[link_index]:
                self.__cs_by_link_and_pos[link_index][pos] = _CrossSection(self.__cs_by_link_and_pos, self.__network)

            self.__cs_by_link_and_pos[link_index][pos].add_data_collection_point(point)

        states = []

        for link_index in self.__cs_by_link_and_pos:
            for position in self.__cs_by_link_and_pos[link_index]:
                cs = self.__cs_by_link_and_pos[link_index][position]
                cs.update_successors()

                self.__cross_sections_by_id[cs.id] = cs

                states.append(cs.get_state())

        print("cross sections created")

        # return self.__network.get_main_route(), states
        return [], states

    async def create_cross_section(self, position: Coordinate,
                                   cs_type: CrossSectionType) -> VissimConnectorCrossSectionState:
        return await self.__push_command(self.__create_cross_section, position, cs_type)

    def __create_cross_section(self, position: Coordinate,
                               cs_type: CrossSectionType) -> VissimConnectorCrossSectionState:
        assert threading.current_thread() == self.__thread

        cross_section = _CrossSection(self.__cs_by_link_and_pos, self.__network)

        self.__add_cs_to_vissim(cross_section, position, cs_type)

        self.__cross_sections_by_id[cross_section.id] = cross_section

        self.__update_all_successors()

        return cross_section.get_state()

    async def remove_cross_section(self, cs_id: str) -> None:
        await self.__push_command(self.__remove_cross_section, cs_id)

    def __remove_cross_section(self, cs_id: str) -> None:
        assert threading.current_thread() == self.__thread

        cross_section = self.__cross_sections_by_id.pop(cs_id)
        self.__remove_cs_from_vissim(cross_section)

        self.__update_all_successors()

    async def move_cross_section(self, cs_id: str, new_position: Coordinate) -> VissimConnectorCrossSectionState:
        return await self.__push_command(self.__move_cross_section, cs_id, new_position)

    def __move_cross_section(self, cs_id: str, new_position: Coordinate) -> VissimConnectorCrossSectionState:
        assert threading.current_thread() == self.__thread

        cross_section = self.__cross_sections_by_id[cs_id]

        # The properties are calculated automatically through the data points, so cache them
        # because deletion will delete the points and therefore reset the properties
        cs_type = cross_section.type
        primary_point_id = cross_section.primary_point_id

        self.__remove_cs_from_vissim(cross_section)
        self.__add_cs_to_vissim(cross_section, new_position, cs_type, primary_point_id)

        assert cross_section.id == cs_id  # If this doesn't hold we get a bunch of problems so better assert it

        self.__update_all_successors()

        return cross_section.get_state()

    def __add_cs_to_vissim(self, cross_section: _CrossSection, position: Coordinate, cs_type: CrossSectionType,
                           first_id: int | None = None) -> None:
        assert threading.current_thread() == self.__thread

        link, pos = self.__network.get_link_and_position(position)

        link_no = link.AttValue("No")

        if link_no not in self.__cs_by_link_and_pos:
            self.__cs_by_link_and_pos[link_no] = {}

        # If this doesn't hold we currently get problems, so assert it for now but maybe TODO conflict detection
        assert pos not in self.__cs_by_link_and_pos[link_no]

        self.__cs_by_link_and_pos[link_no][pos] = cross_section

        data_collection_points = self.__vissim.Net.DataCollectionPoints
        des_speed_decisions = self.__vissim.Net.DesSpeedDecisions

        for lane in link.Lanes.GetAll():
            if cs_type == CrossSectionType.MEASURING or cs_type == CrossSectionType.COMBINED:
                point = data_collection_points.AddDataCollectionPoint(first_id, lane, pos)
                first_id = None
                cross_section.add_data_collection_point(point)

            if cs_type == CrossSectionType.DISPLAY or cs_type == CrossSectionType.COMBINED:
                decision = des_speed_decisions.AddDesSpeedDecision(first_id, lane, pos)
                first_id = None
                cross_section.add_des_speed_decision(decision)

    def __remove_cs_from_vissim(self, cross_section: _CrossSection) -> None:
        assert threading.current_thread() == self.__thread

        self.__cs_by_link_and_pos[cross_section.link_index].pop(cross_section.pos_on_link)

        if not self.__cs_by_link_and_pos[cross_section.link_index]:
            self.__cs_by_link_and_pos.pop(cross_section.link_index)

        point_container = self.__vissim.Net.DataCollectionPoints

        for point in cross_section.data_collection_points:
            point_container.RemoveDataCollectionPoint(point)
            cross_section.remove_data_collection_point(point)

        decision_container = self.__vissim.Net.DesSpeedDecisions

        for decision in cross_section.des_speed_decisions:
            decision_container.RemoveDesSpeedDecision(decision)
            cross_section.remove_des_speed_decision(decision)

    async def init_simulation(self, eval_interval: int) -> tuple[int, int]:
        return await self.__push_command(self.__init_simulation, eval_interval)

    def __init_simulation(self, eval_interval: int) -> tuple[int, int]:
        assert threading.current_thread() == self.__thread

        sim_duration = self.__vissim.Simulation.AttValue('SimPeriod')

        self.__vissim.Net.Evaluation.SetAttValue("DataCollCollectData", 1)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollInterval", eval_interval)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollFromTime", 0)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollToTime", sim_duration)

        self.__vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
        self.__vissim.Simulation.RunSingleStep()
        return 0, sim_duration

    async def continue_simulation(self, span: int) -> None:
        await self.__push_command(self.__continue_simulation, span)

    def __continue_simulation(self, span: int) -> None:
        assert threading.current_thread() == self.__thread

        current_break = self.__vissim.Simulation.AttValue('SimBreakAt')
        self.__vissim.Simulation.SetAttValue('SimBreakAt', current_break + span)
        self.__vissim.Simulation.RunContinuous()

    async def measure(self) -> Input:
        return await self.__push_command(self.__measure)

    def __measure(self) -> Input:
        assert threading.current_thread() == self.__thread

        algo_input = Input()
        for cross_section in self.__cross_sections_by_id.values():
            cross_section.measure(algo_input)

        return algo_input

    async def set_display(self, display: Display) -> None:
        await self.__push_command(self.__set_display, display)

    def __set_display(self, display: Display) -> None:
        assert threading.current_thread() == self.__thread

        for cross_section in self.__cross_sections_by_id.values():
            cross_section.set_display(display)

    async def stop_simulation(self) -> None:
        await self.__push_command(self.__stop_simulation)

    def __stop_simulation(self) -> None:
        assert threading.current_thread() == self.__thread

        self.__vissim.Simulation.Stop()

    async def shutdown(self) -> None:
        await self.__push_command(None)


async def run_test():
    conn = VissimConnector()
    route, css = await conn.load_file(r"C:\Users\vx9186\Projekte\sbaid_old\A5_sarah.inpx")
    # for coord in route:
    #     print(f"{coord.x},{coord.y}")
    for cs in css:
        print(cs)
    # await conn.create_cross_section(Coordinate(0, 0), CrossSectionType.MEASURING)
    # await conn.remove_cross_section(result[-1].id)
    # await conn.move_cross_section(result[-2].id, Coordinate(0, 0))
    # await conn.init_simulation(60)
    # await conn.shutdown()

loop = asyncio.get_event_loop()
task = loop.create_task(run_test())
loop.run_forever()
