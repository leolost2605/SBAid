"""This module defines the SimulationManager class"""
from gi.repository import GObject

from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.network.network import Network
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.results.result_manager import ResultManager


class SimulationManager(GObject.GObject):
    """This class defines the SimulationManager class"""

    def __init__(self, project_name: str, algorithm_configuration: AlgorithmConfiguration,
                 network: Network, simulator: Simulator, result_manager: ResultManager,
                 observer: SimulationObserver) -> None:
        """Initialize the SimulationManager class"""
        super().__init__(project_name=project_name, algorithm_configuration=algorithm_configuration,
                         network=network, simulator=simulator, result_manager=result_manager,
                         observer=observer)

    def cancel(self) -> None:
        """Cancel the simulation"""

    def start(self) -> None:
        """Start the simulation"""
