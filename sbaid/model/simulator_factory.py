"""This module defines the simulator factory."""
import sys

from gi.repository import Gio, GObject

from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.simulator.simulator import Simulator

from sbaid.common.simulator_type import SimulatorType

simulator_types = GObject.Property(type=Gio.ListModel,
                                   flags=GObject.ParamFlags.READABLE |
                                   GObject.ParamFlags.WRITABLE |
                                   GObject.ParamFlags.CONSTRUCT_ONLY)


class SimulatorException(Exception):
    """Exception raised if the given simulator is not supported."""


class InvalidPlatformException(Exception):
    """Exception raised if the given simulator is not supported on the users platform."""


class SimulatorFactory(GObject.GObject):
    """This class defines the simulator factory."""
    def __init__(self) -> None:  # pylint: disable=useless-parent-delegation
        super().__init__()

    def get_simulator(self, sim_type: SimulatorType) -> Simulator:
        """TODO"""
        match sim_type.id:
            case "dummy_json":
                return DummySimulator()
            case "com.ptvgroup.vissim":
                if sys.platform.startswith("win"):
                    # pylint: disable=import-outside-toplevel
                    from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator
                    return VissimSimulator()
                raise InvalidPlatformException("The Vissim simulator requires Windows.")
        raise SimulatorException(f"Simulator type {sim_type.name} is not supported")
