"""
This module contains the project class which represents a SBAid Project
"""

from gi.repository import GObject, GLib

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.project import Project as ModelProject
from sbaid.view_model.simulation import Simulation
from sbaid.view_model.simulation_observer import SimulationObserver


class Project(GObject.Object):
    """
    Represents a SBAid Project. Holds the network as well as the algorithm configuration
    manager as well as some meta information about the project like for example the name.
    """

    __project: ModelProject

    id: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore

    @id.getter  # type: ignore
    def id(self) -> str:
        return self.__project.id

    name: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore

    @name.getter  # type: ignore
    def name(self) -> str:
        return self.__project.name

    simulator_type: SimulatorType = GObject.Property(type=SimulatorType,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE)

    @simulator_type.getter  # type: ignore
    def simulator_type(self) -> SimulatorType:
        return self.__project.simulator_type

    last_modified: GLib.DateTime = GObject.Property(type=GLib.DateTime,  # type: ignore
                                                    flags=GObject.ParamFlags.READABLE)

    @last_modified.getter  # type: ignore
    def last_modified(self) -> GLib.DateTime:
        return self.__project.last_modified

    created_at: GLib.DateTime = GObject.Property(type=GLib.DateTime,  # type: ignore
                                                 flags=GObject.ParamFlags.READABLE)

    @created_at.getter  # type: ignore
    def created_at(self) -> GLib.DateTime:
        return self.__project.created_at

    network: Network = GObject.Property(type=Network,  # type: ignore
                                        flags=GObject.ParamFlags.READABLE |
                                        GObject.ParamFlags.WRITABLE |
                                        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration_manager: AlgorithmConfigurationManager = (
        GObject.Property(type=AlgorithmConfigurationManager,
                         flags=GObject.ParamFlags.READABLE |
                         GObject.ParamFlags.WRITABLE |
                         GObject.ParamFlags.CONSTRUCT_ONLY)
    )

    def __init__(self, project: ModelProject) -> None:
        super().__init__(
            network=Network(project.network),
            algorithm_configuration_manager=AlgorithmConfigurationManager(
                project.algorithm_configuration_manager
            )
        )

        self.__project = project

    def load(self) -> None:
        """
        Loads this project by loading the network and algorithm configuration.
        """
        self.__project.load()

    def start_simulation(self) -> Simulation:
        """
        Starts a simulation with the current configuration and returns an object for
        receiving progress and controlling the simulation.
        :return: an object representing the simulation.
        """

        observer = SimulationObserver()
        manager = self.__project.start_simulation(observer)

        return Simulation(manager, observer)
