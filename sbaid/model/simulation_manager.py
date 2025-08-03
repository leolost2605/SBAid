"""This module defines the SimulationManager class"""
from gi.repository import GObject

from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.network.network import Network
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.results.result_manager import ResultManager


class SimulationManager(GObject.GObject):
    """TODO"""

    def __init__(self, project_name: str, algorithm_configuration: AlgorithmConfiguration,
                 network: Network, simulator: Simulator, result_manager: ResultManager,
                 observer: SimulationObserver) -> None:

        """todo"""

    async def cancel(self) -> None:
        """todo"""

    def start(self) -> None:
        """todo"""
