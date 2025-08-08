"""
This module contains the project class which represents a SBAid Project
"""

from gi.repository import GObject, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.project import Project as ModelProject
from sbaid.view_model.simulation import Simulation
from sbaid.view_model.simulation_observer import SimulationObserver
from sbaid.view_model.network.network import Network
from sbaid.view_model.algorithm_configuration.algorithm_configuration_manager import (
    AlgorithmConfigurationManager)


class Project(GObject.Object):
    """
    Represents a SBAid Project. Holds the network as well as the algorithm configuration
    manager as well as some meta information about the project like for example the name.
    """

    __project: ModelProject

    id: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore

    @id.getter  # type: ignore
    def id(self) -> str:
        """Returns the id of this project"""
        return self.__project.id

    name: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE |  # type: ignore
                                 GObject.ParamFlags.WRITABLE)

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of this project"""
        return self.__project.name

    @name.setter  # type: ignore
    def name(self, name: str) -> None:
        """Sets the name of this project"""
        self.__project.name = name

    simulator_type: SimulatorType = GObject.Property(type=SimulatorType,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE)

    @simulator_type.getter  # type: ignore
    def simulator_type(self) -> SimulatorType:
        """Returns the simulator type of this project"""
        return self.__project.simulator_type

    last_modified: GLib.DateTime = GObject.Property(type=GLib.DateTime,  # type: ignore
                                                    flags=GObject.ParamFlags.READABLE)

    @last_modified.getter  # type: ignore
    def last_modified(self) -> GLib.DateTime:
        """Returns the last modified date of this project"""
        return self.__project.last_modified

    created_at: GLib.DateTime = GObject.Property(type=GLib.DateTime,  # type: ignore
                                                 flags=GObject.ParamFlags.READABLE)

    @created_at.getter  # type: ignore
    def created_at(self) -> GLib.DateTime:
        """Returns the created at date of this project"""
        return self.__project.created_at

    network: Network = GObject.Property(type=Network,  # type: ignore
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration_manager: AlgorithmConfigurationManager = (
        GObject.Property(type=AlgorithmConfigurationManager,  # type: ignore
                         flags=GObject.ParamFlags.READABLE |
                         GObject.ParamFlags.WRITABLE |
                         GObject.ParamFlags.CONSTRUCT_ONLY)
    )

    def __init__(self, project: ModelProject) -> None:
        network = Network(project.network)
        super().__init__(
            network=network,
            algorithm_configuration_manager=AlgorithmConfigurationManager(
                project.algorithm_configuration_manager, network
            )
        )

        self.__project = project

    async def load(self) -> None:
        """
        Loads this project by loading the network and algorithm configuration.
        """
        await self.__project.load()

    async def start_simulation(self) -> Simulation:
        """
        Starts a simulation with the current configuration and returns an object for
        receiving progress and controlling the simulation.
        :return: an object representing the simulation.
        """

        observer = SimulationObserver()  # implements the model simulation observer
        manager = await self.__project.start_simulation(observer)

        return Simulation(manager, observer)
