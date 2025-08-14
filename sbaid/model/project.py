# pylint: disable=too-many-instance-attributes
"""This module defines the Project class."""
from typing import Any

from gi.repository import GObject, GLib, Gio


from sbaid import common
from sbaid.model.simulator.simulator_factory import SimulatorFactory
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


class Project(GObject.GObject):
    """This class defines the Project class. It holds all metadata related to the project,
    as well as references to the individual parts that make up the project. In addition, this
    class is the entry point for a simulation."""

    __project_db: ProjectDatabase
    __simulator: Simulator
    __name: str

    id: str = GObject.Property(type=str,  # type: ignore
                               flags=GObject.ParamFlags.READABLE |
                               GObject.ParamFlags.WRITABLE |
                               GObject.ParamFlags.CONSTRUCT_ONLY)

    name: str = GObject.Property(type=str,  # type: ignore
                                 flags=GObject.ParamFlags.READABLE |
                                 GObject.ParamFlags.WRITABLE)

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the project."""
        return self.__name

    @name.setter  # type: ignore
    def name(self, new_name: str) -> None:
        """Sets the name of the project"""
        self.__name = new_name
        common.run_coro_in_background(self.__project_db.set_project_name(new_name))

    simulator_type: SimulatorType = GObject.Property(type=SimulatorType,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE |
                                                     GObject.ParamFlags.WRITABLE |
                                                     GObject.ParamFlags.CONSTRUCT_ONLY)

    project_file_path: str = GObject.Property(type=str,  # type: ignore
                                              flags=GObject.ParamFlags.READABLE |
                                              GObject.ParamFlags.WRITABLE |
                                              GObject.ParamFlags.CONSTRUCT_ONLY)

    simulation_file_path: str = GObject.Property(type=str,  # type: ignore
                                                 flags=GObject.ParamFlags.READABLE |
                                                 GObject.ParamFlags.WRITABLE |
                                                 GObject.ParamFlags.CONSTRUCT_ONLY)

    created_at: GLib.DateTime = GObject.Property(type=GLib.DateTime,  # type: ignore
                                                 flags=GObject.ParamFlags.READABLE |
                                                 GObject.ParamFlags.WRITABLE)

    last_opened: GLib.DateTime = GObject.Property(type=GLib.DateTime,  # type: ignore
                                                  flags=GObject.ParamFlags.READABLE |
                                                  GObject.ParamFlags.WRITABLE)

    network: Network = GObject.Property(type=Network,  # type: ignore
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration_manager: AlgorithmConfigurationManager = (
        GObject.Property(  # type: ignore
            type=AlgorithmConfigurationManager,
            flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
            GObject.ParamFlags.CONSTRUCT_ONLY))

    result_manager: ResultManager = GObject.Property(type=ResultManager,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE |
                                                     GObject.ParamFlags.WRITABLE |
                                                     GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, project_id: str, sim_type: SimulatorType, simulation_file_path: str,
                 project_file_path: str, result_manager: ResultManager) -> None:
        """Creates a new project. The network and algorithm configuration manager
        are already created, but not yet loaded."""
        project_file = Gio.File.new_for_path(project_file_path)

        self.__project_db = ProjectSQLite(project_file.get_child("db"))

        self.__simulator = SimulatorFactory().get_simulator(sim_type)

        network = Network(self.__simulator, self.__project_db)
        algo_manager = AlgorithmConfigurationManager(network, self.__project_db)

        super().__init__(id=project_id,
                         simulator_type=sim_type,
                         project_file_path=project_file_path,
                         simulation_file_path=simulation_file_path,
                         created_at=GLib.DateTime.new_now_local(),
                         last_opened=GLib.DateTime.new_now_local(),  # TODO: QS
                         network=network,
                         algorithm_configuration_manager=algo_manager,
                         result_manager=result_manager)

        self.__name = "Unknown Project Name"

    async def load(self) -> None:
        """Loads the project, i.e. the algorithm configurations and the network."""
        await self.__simulator.load_file(Gio.File.new_for_path(self.simulation_file_path))
        await self.network.load()
        await self.algorithm_configuration_manager.load()

    async def start_simulation(self, observer: SimulationObserver) -> SimulationManager:
        """Starts a simulation with the currently selected algorithm configuration.
        The transferred observer is regularly informed about the progress of the simulation.
        The returned SimulationManager manages the simulation and can be used to control it."""
        selected_id = self.algorithm_configuration_manager.selected_algorithm_configuration_id

        algo_config = None
        for config in common.list_model_iterator(
                self.algorithm_configuration_manager.algorithm_configurations):
            if config.id == selected_id:
                algo_config = config
                break

        if not algo_config:
            raise AlgorithmConfigurationException("No selected algorithm configuration found!")

        manager = SimulationManager(self.name, algo_config, self.network, self.__simulator,
                                    self.result_manager, observer)
        manager.start()
        return manager

    async def load_from_db(self) -> None:
        """Loads the attributes of the project, such as name and last modification date,
        from the database."""
        await self.__project_db.open()
        name = await self.__project_db.get_project_name()
        if name is not None:
            self.__name = name
        created_at = await self.__project_db.get_created_at()
        if created_at is not None:
            self.created_at = created_at
        last_opened = await self.__project_db.get_last_opened()
        if last_opened is not None:
            self.last_opened = last_opened  # TODO: QS

    async def delete(self) -> None:
        """Deletes the project database file."""
        # TODO: Delete whole folder
        file = Gio.File.new_for_path(self.project_file_path).get_child("db")
        file.delete_async(GLib.PRIORITY_DEFAULT, None, self.__on_delete)

    def __on_delete(self, source_object: Gio.File, result: Gio.AsyncResult, user_data: Any) -> None:
        """File deletion callback."""
        source_object.delete_finish(result)
