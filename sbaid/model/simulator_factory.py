"""This module defines the simulator factory."""
import sys

from gi.repository import Gio, GObject

from model.simulator.dummy.dummy_simulator import DummySimulator
from model.simulator.simulator import Simulator

from sbaid.common.simulator_type import SimulatorType

simulator_types = GObject.Property(type=Gio.ListModel,
                                   flags=GObject.ParamFlags.READABLE |
                                   GObject.ParamFlags.WRITABLE |
                                   GObject.ParamFlags.CONSTRUCT_ONLY)


class SimulatorException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidPlatformException(Exception):
    """TODO"""
    def __init__(self, message: str):
        super().__init__(message)


class SimulatorFactory(GObject.GObject):
    """This class defines the simulator factory."""
    def __init__(self) -> None:
        # super().__init__(simulator_types=Gio.ListStore(SimulatorType))
        super().__init__()

    def get_simulator(self, sim_type: SimulatorType) -> Simulator:
        match sim_type.id:
            case "dummy_json":
                return DummySimulator()
            case "com.ptvgroup.vissim":
                if sys.platform.startswith("win"):
                    from model.simulator.vissim.vissim_simulator import VissimSimulator
                    return VissimSimulator()
                raise InvalidPlatformException("The Vissim simulator requires Windows.")
        raise SimulatorException(f"Simulator type {SimulatorType.name} is not supported")
