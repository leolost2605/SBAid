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
    __data_collection_points: list[Any] = []
    __des_speed_decisions: list[Any] = []

    @property
    def id(self) -> str:
        if self.__data_collection_points:
            return str(self.__data_collection_points[0].AttVal("No"))

        return str(self.__des_speed_decisions[0].AttVal("No"))

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

    def add_point(self, point: Any) -> None:
        self.__data_collection_points.append(point)

    def get_state(self) -> VissimConnectorCrossSectionState:
        return VissimConnectorCrossSectionState(self.id, self.type, self.position, self.lanes)


class VissimConnector:
    _vissim: Any  # For the COM interface we use dynamic typing
    __cross_sections: dict[int, dict[float, VissimConnectorCrossSection]] = {}

    def __init__(self, queue: Queue[VissimCommand]) -> None:
        pythoncom.CoInitialize()

        while self._handle_command(queue.get()):
            pass

    def _handle_command(self, command: VissimCommand) -> bool:
        args: tuple[Any, ...] | None = None

        match command.type:
            case VissimCommandType.LOAD_FILE:
                self._start_vissim()
                self._load_network(command.kwargs["path"])
                args = (self._get_cross_sections(),)

            case VissimCommandType.INIT_SIMULATION:
                args = self._init_simulation()

            case VissimCommandType.SHUTDOWN:
                pass

        if args is None:
            command.finish()
        else:
            command.finish(*args)

        return command.type != VissimCommandType.SHUTDOWN

    def _start_vissim(self) -> None:
        try:
            self._vissim = com.gencache.EnsureDispatch("Vissim.Vissim")
        except Exception as e:
            raise VissimNotFoundException(e)

    def _load_network(self, path: str) -> None:
        self._vissim.LoadNet(path, False)

    def _get_cross_sections(self) -> list[VissimConnectorCrossSectionState]:
        points = self._vissim.Net.DataCollectionPoints.GetAll()

        if not points:
            return []

        for point in points:
            link_index = point.Lane.Link.AttValue("No")
            pos = point.AttValue("Pos")

            if not link_index in self.__cross_sections:
                self.__cross_sections[link_index] = {}

            if not pos in self.__cross_sections[link_index]:
                self.__cross_sections[link_index][pos] = VissimConnectorCrossSection()

            self.__cross_sections[link_index][pos].add_point(point)

        cross_sections = []

        for link_index in self.__cross_sections:
            for position in self.__cross_sections[link_index]:
                cross_sections.append(self.__cross_sections[link_index][position].get_state())

        return cross_sections

    def _init_simulation(self) -> tuple[int, int]:
        sim_duration = self._vissim.Simulation.AttValue('SimPeriod')
        self._vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
        self._vissim.Simulation.RunSingleStep()
        return 0, sim_duration


async def main() -> None:
    man = VissimManager()
    await man.load_file(r"C:\Users\vx9186\Projekte\SBAid\Beispieldaten_Vissim\Beispieldaten_Vissim\A5_sarah.inpx")
    # print(await man.init_simulation())
    await man.shutdown()


asyncio.run(main())
