# pylint: disable=too-many-instance-attributes
"""This module defines the Project class."""

from gi.repository import GObject, GLib, Gio


from sbaid.model.simulator_factory import SimulatorFactory
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
import sbaid.common


class AlgorithmConfigurationException(Exception):
    """Exception raised when an algorithm configuration is invalid."""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Project(GObject.GObject):
    """This class defines the Project class. It holds all metadata related to the project,
    as well as references to the individual parts that make up the project. In addition, this
    class is the entry point for a simulation."""

    __project_db: ProjectDatabase

    id = GObject.Property(type=str,
                          flags=GObject.ParamFlags.READABLE |
                          GObject.ParamFlags.WRITABLE |
                          GObject.ParamFlags.CONSTRUCT_ONLY)

    name = GObject.Property(type=str,
                            flags=GObject.ParamFlags.READABLE |
                            GObject.ParamFlags.WRITABLE |
                            GObject.ParamFlags.CONSTRUCT)

    simulator_type = GObject.Property(type=SimulatorType,
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT_ONLY)

    project_file_path = GObject.Property(type=str,
                                         flags=GObject.ParamFlags.READABLE |
                                         GObject.ParamFlags.WRITABLE |
                                         GObject.ParamFlags.CONSTRUCT_ONLY)

    simulation_file_path = GObject.Property(type=str,
                                            flags=GObject.ParamFlags.READABLE |
                                            GObject.ParamFlags.WRITABLE |
                                            GObject.ParamFlags.CONSTRUCT_ONLY)

    created_at = GObject.Property(type=GLib.DateTime,
                                  flags=GObject.ParamFlags.READABLE |
                                  GObject.ParamFlags.WRITABLE |
                                  GObject.ParamFlags.CONSTRUCT_ONLY)

    last_modified = GObject.Property(type=GLib.DateTime,
                                     flags=GObject.ParamFlags.READABLE |
                                     GObject.ParamFlags.WRITABLE |
                                     GObject.ParamFlags.CONSTRUCT)

    simulator = GObject.Property(type=Simulator,
                                 flags=GObject.ParamFlags.READABLE |
                                 GObject.ParamFlags.WRITABLE |
                                 GObject.ParamFlags.CONSTRUCT_ONLY)

    network = GObject.Property(type=Network,
                               flags=GObject.ParamFlags.READABLE |
                               GObject.ParamFlags.WRITABLE |
                               GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration_manager = GObject.Property(type=AlgorithmConfigurationManager,
                                                       flags=GObject.ParamFlags.READABLE |
                                                       GObject.ParamFlags.WRITABLE |
                                                       GObject.ParamFlags.CONSTRUCT_ONLY)

    result_manager = GObject.Property(type=ResultManager,
                                      flags=GObject.ParamFlags.READABLE |
                                      GObject.ParamFlags.WRITABLE |
                                      GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, project_id: str, sim_type: SimulatorType, simulation_file_path: str,
                 project_file_path: str, result_manager: ResultManager) -> None:
        """Creates a new project. The network and algorithm configuration manager
        are already created, but not yet loaded."""
        simulator = SimulatorFactory().get_simulator(sim_type)
        project_file = Gio.File.new_for_path(project_file_path)
        self.__project_db = ProjectSQLite(project_file.get_child(self.id))
        network = Network(simulator, self.__project_db)
        algo_manager = AlgorithmConfigurationManager(network)
        super().__init__(id=project_id, name=project_id+"name",
                         simulator_type=sim_type, project_file_path=project_file_path,
                         simulation_file_path=simulation_file_path,
                         created_at=GLib.DateTime.new_now_local(),
                         last_modified=GLib.DateTime.new_now_local(),
                         simulator=simulator,
                         network=network,
                         algorithm_configuration_manager=algo_manager,
                         result_manager=result_manager)

    async def load(self) -> None:
        """Loads the project, i.e. the algorithm configurations and the network."""
        await self.network.load()
        if not self.algorithm_configuration_manager:
            return  # TODO
        self.algorithm_configuration_manager.load()

    async def start_simulation(self, observer: SimulationObserver) -> SimulationManager:
        """Starts a simulation with the currently selected algorithm configuration.
        The transferred observer is regularly informed about the progress of the simulation.
        The returned SimulationManager manages the simulation and can be used to control it."""
        selected_algorithm_configuration_id = (self.algorithm_configuration_manager
                                               .selected_algorithm_configuration_id)
        algo_config = None
        for config in sbaid.common.list_model_iterator(self.algorithm_configuration_manager
                                                       .algorithm_configurations):
            if config.id == selected_algorithm_configuration_id:
                algo_config = config
        if not algo_config:
            raise AlgorithmConfigurationException("No selected algorithm configuration found!")

        _simulation_manager = SimulationManager(self.name, algo_config,
                                                self.network, self.simulator,
                                                self.result_manager, observer)
        await _simulation_manager.start()
        return _simulation_manager

    async def load_from_db(self) -> None:
        """Loads the attributes of the project, such as name and last modification date,
        from the database."""
        async with self.__project_db as db:
            self.name = await db.get_project_name()
            self.last_modified = await db.get_last_modified()
