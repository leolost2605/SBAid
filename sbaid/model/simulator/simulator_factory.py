"""This module defines the simulator factory."""
import sys

from gi.repository import Gio, GObject

import sbaid.model.simulator.vissim.vissim_simulator
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.simulator.simulator import Simulator

from sbaid.common.simulator_type import SimulatorType

simulator_types = GObject.Property(type=Gio.ListModel,
                                   flags=GObject.ParamFlags.READABLE |
                                   GObject.ParamFlags.WRITABLE |
                                   GObject.ParamFlags.CONSTRUCT_ONLY)


class SimulatorException(Exception):
    """Exception raised if the given simulator is not supported."""


class SimulatorFactory(GObject.GObject):
    """This class defines the simulator factory."""

    __types: Gio.ListStore

    simulator_types: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore

    def __init__(self) -> None:
        super().__init__()

        self.__types = Gio.ListStore.new(SimulatorType)
        self.__types.append(DummySimulator().type)

        if sys.platform.startswith("win"):
            self.__types.append(
                sbaid.model.simulator.vissim.vissim_simulator.VissimSimulator().type)

    def get_simulator(self, sim_type: SimulatorType) -> Simulator:
        """
        Returns the simulator implementation for the given type
        :param sim_type: the type of the simulator to construct
        :return: the simulator implementation of the given type
        """

        if sim_type.id is DummySimulator().type.id:
            return DummySimulator()

        if sys.platform.startswith("win"):
            # pylint: disable=import-outside-toplevel
            from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator

            if sim_type.id is VissimSimulator().type.id:
                return VissimSimulator()

        raise SimulatorException(f"Simulator type {sim_type.name} not found")
