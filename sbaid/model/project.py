"""This module defines the Project class."""
from gi.repository import GObject, GLib
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.simulation_manager import SimulationManager
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import (
    AlgorithmConfigurationManager)
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.network.network import Network


class Project(GObject.GObject):
    """This class defines the Project class. It holds all metadata related to the project,
    as well as references to the individual parts that make up the project. In addition, this
    class is the entry point for a simulation."""

    id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    simulator_type = GObject.Property(
        type=SimulatorType,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    project_file_path = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    simulation_file_path = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    created_at = GObject.Property(
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    last_modified = GObject.Property(
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    simulator = GObject.Property(
        type=Simulator,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    network = GObject.Property(
        type=Network,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration_manager = GObject.Property(
        type=AlgorithmConfigurationManager,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, project_id: str, sim_type: SimulatorType, simulation_file_path: str,
                 project_file_path: str, project_db: ProjectDatabase) -> None:
        """Creates a new project. The network and algorithm configuration manager
        are already created, but not yet loaded."""
        # self.__project_db = project_db
        super().__init__(id=project_id, simulator_type=sim_type,
                         simulation_file_path=simulation_file_path,
                         project_file_path=project_file_path)
        # TODO the constructor needs to be fixed

    def load(self) -> None:
        """Loads the project, i.e. the algorithm configurations and the network."""
        self.network.load()
        self.algorithm_configuration_manager.load()

    def start_simulation(self, observer: SimulationObserver) -> SimulationManager:
        """Starts a simulation with the currently selected algorithm configuration.
        The transferred observer is regularly informed about the progress of the simulation.
        The returned SimulationManager manages the simulation and can be used to control it."""
        algorithm_configuration = (self.algorithm_configuration_manager
                                   .get_algorithm_configurations())
        result_manager = ResultManager()
        simulation_manager = SimulationManager(self.name, algorithm_configuration,
                                               self.network, self.simulator,
                                               result_manager, observer)
        simulation_manager.start()
        return simulation_manager

    async def load_from_db(self) -> None:
        """Loads the attributes of the project, such as name and last modification date,
        from the database."""
        # todo: check privacy
