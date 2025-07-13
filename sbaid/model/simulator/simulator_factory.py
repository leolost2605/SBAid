"""This module contains the factory for different simulators"""
from sbaid.common.simulator_type import SimulatorType
from .simulator import Simulator


class SimulatorFactory:
    """Factory class for creating simulator instances."""

    def get_simulator(self, simulator_type: SimulatorType) -> Simulator:
        """Factory method for creating simulator instances."""
        return None
