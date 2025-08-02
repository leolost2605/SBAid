"""This module defines the Project class."""
from gi.repository import GObject, GLib, Gtk
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.algorithm.algorithm import Algorithm
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.network.cross_section import CrossSection
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
        self.__project_db = project_db
        super().__init__(id=project_id, simulator_type=sim_type,
                         simulation_file_path=simulation_file_path,
                         project_file_path=project_file_path)

    def load(self) -> None:
        """Loads the project, i.e. the algorithm configurations and the network."""
        self.network.load()
        sim_cross_sections = self.network.observe_cross_sections()
        self.network.set_list_model(sim_cross_sections)
        for sim_cross_section in sim_cross_sections:
            self.network.Gtk.MapListModel.map_func(sim_cross_section)
            cross_section = CrossSection(sim_cross_section)
            self.network.load()
            cs_name = self.__project_db.get_cross_section_name(cross_section.id)

        self.algorithm_configuration_manager.load()
        list_algo_config_ids = self.__project_db.get_all_algorithm_configuration_ids()
        selected_algo_config_id = self.__project_db.get_selected_algorithm_configuration_id()
        algorithm_configurations = Gtk.ListModel()

        for id in list_algo_config_ids:
            algo_config = AlgorithmConfiguration(id, self.network)
            param_config = ParameterConfiguration(self.network)
            parameters = Gtk.FlattenListModel()
            name, evaluation_interval, display_interval, script_path = self.__project_db.get_algorithm_configuration(id)
            algo_config.load_algorithm(script_path)  # todo no load algorithm in algo class
            algo_config.algorithm = Algorithm()
            param_config.set_algorithm(algo_config.algorithm)
            algorithm_configurations.append(algo_config)


    def start_simulation(self, observer: SimulationObserver) -> SimulationManager:
        """Starts a simulation with the currently selected algorithm configuration. The transferred observer
        is regularly informed about the progress of the simulation. The returned
        SimulationManager manages the simulation and can be used to control it."""
        algorithm_configuration = self.algorithm_configuration_manager.get_algorithm_configurations()
        result_manager = ResultManager()
        simulation_manager = SimulationManager(self.name, algorithm_configuration,
                                               self.network, self.simulator, result_manager, observer)
        simulation_manager.start()
        return simulation_manager

    def load_from_db(self) -> None:
        """Loads the attributes of the project, such as name and last modification date,
        from the database."""
        """todo: check privacy"""

