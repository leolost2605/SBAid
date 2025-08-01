"""This module defines the Project class."""
from gi.repository import GObject, GLib, Gio

import sbaid.common
from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.database.project_sqlite import ProjectSQLite
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.simulation_manager import SimulationManager
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import (
    AlgorithmConfigurationManager)
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.network.network import Network


class AlgorithmConfigurationException(Exception):
    """Exception raised when an algorithm configuration is invalid."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Project(GObject.GObject):
    """This class defines the Project class. It holds all metadata related to the project,
    as well as references to the individual parts that make up the project. In addition, this
    class is the entry point for a simulation."""

    __project_db: ProjectDatabase

    __id: str
    __name: str
    __simulator_type: SimulatorType
    __project_file_path: str
    __simulation_file_path: str
    __created_at: GLib.DateTime
    __last_modified: GLib.DateTime
    __simulator: Simulator
    __network: Network
    __algorithm_configuration_manager: AlgorithmConfigurationManager

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    def id(self):
        return self.__id

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)
    def name(self):
        return self.__name

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def simulator_type(self):
        return self.__simulator_type

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def project_file_path(self):
        return self.__project_file_path

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def simulation_file_path(self):
        return self.__simulation_file_path

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def created_at(self):
        return self.__created_at

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT)
    def last_modified(self):
        return self.__last_modified

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def simulator(self):
        return self.__simulator

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def network(self):
        return self.__network

    @GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
              GObject.ParamFlags.WRITABLE |
              GObject.ParamFlags.CONSTRUCT_ONLY)
    def algorithm_configuration_manager(self):
        return self.__algorithm_configuration_manager

    def __init__(self, project_id: str, sim_type: SimulatorType, simulation_file_path: str,
                 project_file_path: str) -> None:
        """Creates a new project. The network and algorithm configuration manager
        are already created, but not yet loaded."""
        self.__id = project_id
        self.__name = self.__id + "name"
        self.__simulator_type = sim_type
        self.__simulation_file_path = simulation_file_path
        self.__created_at = GLib.DateTime.new_now_local()
        self.__last_modified = GLib.DateTime.new_now_local()
        self.__project_file_path = project_file_path
        project_file = Gio.File.new_for_path(project_file_path)
        self.__project_db = ProjectSQLite(project_file.get_child(self.id))

        super().__init__()

    def load(self) -> None:
        """Loads the project, i.e. the algorithm configurations and the network."""
        self.network.load()
        self.algorithm_configuration_manager.load()

    def start_simulation(self, observer: SimulationObserver) -> SimulationManager:
        """Starts a simulation with the currently selected algorithm configuration.
        The transferred observer is regularly informed about the progress of the simulation.
        The returned SimulationManager manages the simulation and can be used to control it."""
        algorithm_configuration_id = (self.algorithm_configuration_manager
                                      .selected_algorithm_configuration_id)
        algo_config = None
        for config in sbaid.common.list_model_iterator(self.algorithm_configuration_manager
                                                       .algorithm_configurations):
            if config.id == algorithm_configuration_id:
                algo_config = config
        if not algo_config:
            raise AlgorithmConfigurationException("No selected algorithm configuration found!")

        result_manager = ResultManager()
        simulation_manager = SimulationManager(self.name, algo_config,
                                               self.network, self.simulator,
                                               result_manager, observer)
        simulation_manager.start()
        return simulation_manager

    async def load_from_db(self) -> None:
        """Loads the attributes of the project, such as name and last modification date,
        from the database."""
        async with self.__project_db as db:
            self.name = await db.get_project_name()
            self.last_modified = await db.get_last_modified()
