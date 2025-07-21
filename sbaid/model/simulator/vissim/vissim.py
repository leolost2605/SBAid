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


class _CrossSection:
    data_collection_points: list[Any]
    des_speed_decisions: list[Any]

    def __init__(self):
        self.data_collection_points = []
        self.des_speed_decisions = []

    @property
    def main_id(self) -> int:
        if self.data_collection_points:
            return self.data_collection_points[0].AttValue("No")

        return self.des_speed_decisions[0].AttValue("No")

    @property
    def type(self) -> CrossSectionType:
        if not self.des_speed_decisions:
            return CrossSectionType.MEASURING

        if not self.data_collection_points:
            return CrossSectionType.DISPLAY

        return CrossSectionType.COMBINED

    @property
    def position(self) -> Coordinate:
        return None

    @property
    def lanes(self) -> int:
        if self.data_collection_points:
            return len(self.data_collection_points)

        return len(self.des_speed_decisions)

    def add_data_collection_point(self, point: Any) -> None:
        self.data_collection_points.append(point)

    def add_des_speed_decision(self, des_speed_decision: Any) -> None:
        self.des_speed_decisions.append(des_speed_decision)

    def get_state(self) -> VissimConnectorCrossSectionState:
        return VissimConnectorCrossSectionState(str(self.main_id), self.type, self.position, self.lanes)

    def measure(self, algo_input: Input) -> None:
        for i, point in enumerate(self.data_collection_points):
            cs_id = self.main_id
            lane_index = point.Lane.AttValue("Index") - 1
            for measurement in point.DataCollMeas.GetAll():
                avg_speed = measurement.AttValue("SpeedAvgArith(Current,Last,All)")
                print(f"avg speed for {cs_id} on lane {lane_index} : {avg_speed}")

    def set_display(self, display: Display) -> None:
        if not self.des_speed_decisions:
            return

        for decision in self.des_speed_decisions:
            lane_index = decision.Lane.AttValue("Index") - 1
            a_display = display.get_a_display(self.main_id, lane_index)
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
            # TODO: neighbor_lane.SetAttValue("NoLnChRAllVehTypes", True)


class VissimConnector:
    __thread: Thread
    __queue: Queue[VissimCommand]
    __vissim: Any  # For the COM interface we use dynamic typing
    __network: VissimNetwork | None
    __cross_sections_by_id: dict[str, _CrossSection] = {}

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

    async def load_file(self, path: str) -> list[VissimConnectorCrossSectionState]:
        return await self.__push_command(self.__load_file, path)

    def __load_file(self, path: str) -> list[VissimConnectorCrossSectionState]:
        assert threading.current_thread() == self.__thread

        try:
            self.__vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
        except Exception as e:
            raise VissimNotFoundException(e)

        self.__vissim.LoadNet(path, False)
        self.__network = VissimNetwork(self.__vissim.Net)

        points = self.__vissim.Net.DataCollectionPoints.GetAll()

        if not points:
            return []

        cs_by_link_id_and_pos = {}

        for point in points:
            link_index = point.Lane.Link.AttValue("No")
            pos = point.AttValue("Pos")

            if link_index not in cs_by_link_id_and_pos:
                cs_by_link_id_and_pos[link_index] = {}

            if pos not in cs_by_link_id_and_pos[link_index]:
                cs_by_link_id_and_pos[link_index][pos] = _CrossSection()

            cs_by_link_id_and_pos[link_index][pos].add_data_collection_point(point)

        cross_section_states = []

        for link_index in cs_by_link_id_and_pos:
            for position in cs_by_link_id_and_pos[link_index]:
                cross_section_states.append(cs_by_link_id_and_pos[link_index][position].get_state())

        return cross_section_states

    async def create_cross_section(self, position: Coordinate,
                                   cs_type: CrossSectionType) -> VissimConnectorCrossSectionState:
        return await self.__push_command(self.__create_cross_section, position, cs_type)

    def __create_cross_section(self, position: Coordinate,
                               cs_type: CrossSectionType) -> VissimConnectorCrossSectionState:
        assert threading.current_thread() == self.__thread

        cross_section = _CrossSection()

        self.__add_cs_to_vissim(position, cs_type, cross_section)

        return cross_section.get_state()

    async def remove_cross_section(self, cs_id: str) -> None:
        await self.__push_command(self.__remove_cross_section, cs_id)

    def __remove_cross_section(self, cs_id: str) -> None:
        assert threading.current_thread() == self.__thread

        cross_section = self.__cross_sections_by_id.pop(cs_id)
        self.__remove_cs_from_vissim(cross_section)

    async def move_cross_section(self, cs_id: str, new_position: Coordinate) -> VissimConnectorCrossSectionState:
        return await self.__push_command(self.__move_cross_section, cs_id, new_position)

    def __move_cross_section(self, cs_id: str, new_position: Coordinate) -> VissimConnectorCrossSectionState:
        assert threading.current_thread() == self.__thread

        cross_section = self.__cross_sections_by_id[cs_id]

        # The properties are calculated automatically through the data points, so cache them
        # because deletion will delete the points and therefore reset the properties
        cs_type = cross_section.type
        main_id = cross_section.main_id

        self.__remove_cs_from_vissim(cross_section)
        self.__add_cs_to_vissim(new_position, cs_type, cross_section, main_id)

        return cross_section.get_state()

    def __add_cs_to_vissim(self, position: Coordinate, cs_type: CrossSectionType,
                           cross_section: _CrossSection,
                           first_id: int | None = None) -> None:
        assert threading.current_thread() == self.__thread

        link, pos = self.__network.get_link_and_position(position)

        data_collection_points = self.__vissim.Net.DataCollectionPoints
        des_speed_decisions = self.__vissim.Net.DesSpeedDecisions

        for lane in link.Lanes.GetAll(): #TODO: Check whether None works
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

        point_container = self.__vissim.Net.DataCollectionPoints

        for point in cross_section.data_collection_points:
            point_container.RemoveDataCollectionPoint(point)

        cross_section.data_collection_points.clear()

        decision_container = self.__vissim.Net.DesSpeedDecisions

        for decision in cross_section.des_speed_decisions:
            decision_container.RemoveDesSpeedDecision(decision)

        cross_section.des_speed_decisions.clear()

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
    result = await conn.load_file(r"C:\Users\vx9186\Projekte\sbaid_old\A5_sarah.inpx")
    for cs in result:
        print(cs)
    # await conn.init_simulation(60)
    await conn.shutdown()

asyncio.run(run_test())
