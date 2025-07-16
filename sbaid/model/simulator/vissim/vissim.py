"""TODO"""
import _thread

import win32com.client as com
import asyncio
import pythoncom
from queue import Queue
from enum import Enum
from typing import Any, Optional
from threading import Thread


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


class VissimConnector:
    _vissim: Any  # For the COM interface we use dynamic typing

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

    def _init_simulation(self) -> tuple[int, int]:
        sim_duration = self._vissim.Simulation.AttValue('SimPeriod')
        self._vissim.Simulation.SetAttValue('UseMaxSimSpeed', True)
        self._vissim.Simulation.RunSingleStep()
        return 0, sim_duration


async def main() -> None:
    man = VissimManager()
    await man.load_file(r"C:\Users\Public\Documents\PTV Vision\PTV Vissim 2025\Examples Demo\3D - Complex Intersection Karlsruhe.DE\Karlsruhe 3D.inpx")
    print(await man.init_simulation())
    await man.shutdown()


asyncio.run(main())
