"""TODO"""
import win32com.client as com
import asyncio
import pythoncom
from queue import Queue
from enum import Enum
from typing import Any, NamedTuple
from threading import Thread

from sbaid.common.coordinate import Coordinate
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulation.input import Input
from sbaid.model.simulator.vissim.vissim_network import VissimNetwork
from sbaid.model.simulator.vissim.vissim_cross_section import VissimCrossSection


class VissimNotFoundException(Exception):
    pass


class VissimCommandType(Enum):
    LOAD_FILE = 0,
    INIT_SIMULATION = 1,
    SHUTDOWN = 2


class VissimCommand:
    future: asyncio.Future[tuple[Any, ...]]

    def __init__(self, command_type: VissimCommandType, **kwargs: Any) -> None:
        self.future = asyncio.get_event_loop().create_future()
        self.type = command_type
        self.kwargs = kwargs

    def finish(self, *results: Any) -> None:
        self.future.get_loop().call_soon_threadsafe(self.future.set_result, results)


class VissimConnectorCrossSectionState(NamedTuple):
    id: str
    type: CrossSectionType
    position: Coordinate
    lanes: int


class CommandQueue(Queue):
    async def _put_command(self, command_type: VissimCommandType, **kwargs) -> tuple[Any, ...]:
        command = VissimCommand(command_type, **kwargs)
        self.put(command)
        return await command.future

    async def load_file(self, path: str) -> list[VissimConnectorCrossSectionState]:
        return await self._put_command(VissimCommandType.LOAD_FILE, path=path)

    async def init_simulation(self) -> tuple[int, int]:
        return await self._put_command(VissimCommandType.INIT_SIMULATION)

    async def shutdown(self) -> None:
        await self._put_command(VissimCommandType.SHUTDOWN)

class VissimManager:
    _command_queue: Queue[VissimCommand]
    _thread: Thread

    def __init__(self) -> None:
        self._command_queue = Queue()

        thread = Thread(target=VissimConnector, args=(self._command_queue,), daemon=True)
        thread.start()
        self._thread = thread

    def _push_command(self, command_type: VissimCommandType, **kwargs: Any) -> VissimCommand:
        command = VissimCommand(command_type, **kwargs)
        self._command_queue.put(command)
        return command

    async def shutdown(self) -> None:
        await self._push_command(VissimCommandType.SHUTDOWN).future

    async def load_file(self, path: str) -> None:
        await self._push_command(VissimCommandType.LOAD_FILE, path=path).future

    async def init_simulation(self) -> tuple[int, int]:
        return await self._push_command(VissimCommandType.INIT_SIMULATION).future


class VissimConnectorCrossSection:
    data_collection_points: list[Any] = []
    des_speed_decisions: list[Any] = []

    @property
    def main_id(self) -> int:
        if self.data_collection_points:
            return self.data_collection_points[0].AttVal("No")

        return self.des_speed_decisions[0].AttVal("No")

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
        for point in self.data_collection_points:
            cs_id = self.main_id
            lane_index = point.Lane.AttValue("Index")
            for measurement in point.DataCollMeas.GetAll():
                avg_speed = measurement.AttVal("SpeedAvgArith(Current,Last,All)")
                print(f"avg speed for {cs_id} on lane {lane_index} : {avg_speed}")


class VissimConnector:
    __thread: Thread
    __vissim: Any  # For the COM interface we use dynamic typing
    __network: VissimNetwork | None
    __cross_sections: dict[int, dict[float, VissimConnectorCrossSection]] = {}
    __cross_sections_by_id: dict[str, VissimConnectorCrossSection] = {}

    def __init__(self, queue: Queue[VissimCommand]) -> None:
        self.__thread = Thread(target=self.__thread_func, args=(queue,), daemon=True)
        self.__thread.start()

    def __thread_func(self, queue: Queue[VissimCommand]) -> None:
        pythoncom.CoInitialize()

        while self.__handle_command(queue.get()):
            pass

        self.__vissim.Exit()
        self.__vissim = None
        self.__network = None
        pythoncom.CoUninitialize()

    def __handle_command(self, command: VissimCommand) -> bool:
        args: tuple[Any, ...] | None = None

        match command.type:
            case VissimCommandType.LOAD_FILE:
                self.__start_vissim()
                self.__load_network(command.kwargs["path"])
                args = (self.__get_cross_sections(),)

            case VissimCommandType.INIT_SIMULATION:
                args = self.__init_simulation()

            case VissimCommandType.SHUTDOWN:
                pass

        if args is None:
            command.finish()
        else:
            command.finish(*args)

        return command.type != VissimCommandType.SHUTDOWN

    def __start_vissim(self) -> None:
        try:
            self.__vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
        except Exception as e:
            raise VissimNotFoundException(e)

    def __load_network(self, path: str) -> None:
        self.__vissim.LoadNet(path, False)
        self.__network = VissimNetwork(self.__vissim.Net)

    def __get_cross_sections(self) -> list[VissimConnectorCrossSectionState]:
        points = self.__vissim.Net.DataCollectionPoints.GetAll()

        if not points:
            return []

        for point in points:
            link_index = point.Lane.Link.AttValue("No")
            pos = point.AttValue("Pos")

            if not link_index in self.__cross_sections:
                self.__cross_sections[link_index] = {}

            if not pos in self.__cross_sections[link_index]:
                self.__cross_sections[link_index][pos] = VissimConnectorCrossSection()

            self.__cross_sections[link_index][pos].add_data_collection_point(point)

        cross_sections = []

        for link_index in self.__cross_sections:
            for position in self.__cross_sections[link_index]:
                cross_sections.append(self.__cross_sections[link_index][position].get_state())

        return cross_sections

    def __create_cross_section(self, position: Coordinate,
                               cs_type: CrossSectionType) -> VissimConnectorCrossSection:
        cross_section = VissimConnectorCrossSection()

        self.__add_cs_to_vissim(position, cs_type, cross_section)

        return cross_section

    def __move_cross_section(self, cs_id: str, new_position: Coordinate) -> None:
        cross_section = self.__cross_sections_by_id[cs_id]

        # The properties are calculated automatically through the data points, so cache them
        # because deletion will delete the points and therefore reset the properties
        cs_type = cross_section.type
        main_id = cross_section.main_id

        self.__remove_cs_from_vissim(cross_section)
        self.__add_cs_to_vissim(new_position, cs_type, cross_section, main_id)

    def __delete_cross_section(self, cs_id: str) -> None:
        cross_section = self.__cross_sections_by_id.pop(cs_id)
        self.__remove_cs_from_vissim(cross_section)

    def __add_cs_to_vissim(self, position: Coordinate, cs_type: CrossSectionType,
                           cross_section: VissimConnectorCrossSection,
                           first_id: int | None = None) -> None:
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

    def __remove_cs_from_vissim(self, cross_section: VissimConnectorCrossSection) -> None:
        point_container = self.__vissim.Net.DataCollectionPoints

        for point in cross_section.data_collection_points:
            point_container.RemoveDataCollectionPoint(point)

        cross_section.data_collection_points.clear()

        decision_container = self.__vissim.Net.DesSpeedDecisions

        for decision in cross_section.des_speed_decisions:
            decision_container.RemoveDesSpeedDecision(decision)

        cross_section.des_speed_decisions.clear()

    def __init_simulation(self, eval_interval: int) -> tuple[int, int]:
        sim_duration = self.__vissim.Simulation.AttValue('SimPeriod')

        self.__vissim.Net.Evaluation.SetAttValue("DataCollCollectData", 1)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollInterval", eval_interval)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollFromTime", 0)
        self.__vissim.Net.Evaluation.SetAttValue("DataCollToTime", sim_duration)

        self.__vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
        self.__vissim.Simulation.RunSingleStep()
        return 0, sim_duration

    def __continue_simulation(self, span: int) -> None:
        current_break = self.__vissim.Simulation.AttValue('SimBreakAt')
        self.__vissim.Simulation.SetAttValue('SimBreakAt', current_break + span)
        self.__vissim.Simulation.RunContinuous()

    def __measure(self) -> Input:
        algo_input = Input()
        for cross_section in self.__cross_sections_by_id.values():
            cross_section.measure(algo_input)

        return algo_input

    def __stop_simulation(self) -> None:
        self.__vissim.Simulation.Stop()


async def main() -> None:
    man = VissimManager()
    await man.load_file(r"C:\Users\vx9186\Projekte\SBAid\Beispieldaten_Vissim\Beispieldaten_Vissim\A5_sarah.inpx")
    # print(await man.init_simulation())
    await man.shutdown()


asyncio.run(main())
