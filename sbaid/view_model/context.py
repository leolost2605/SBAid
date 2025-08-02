"""
Contains the context class which holds the projects and result manager.
"""

import sys

import gi

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context as ModelContext
from sbaid.model.project import Project as ModelProject
from sbaid.view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gio, GObject, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Context(GObject.Object):
    """
    Manages the projects and holds the result manager.
    """

    __context: ModelContext

    result_manager: ResultManager = GObject.Property(type=ResultManager,
                                                     flags=GObject.ParamFlags.READABLE |
                                                     GObject.ParamFlags.WRITABLE |
                                                     GObject.ParamFlags.CONSTRUCT_ONLY)

    projects: Gio.ListModel = GObject.Property(type=Gio.ListModel,
                                               flags=GObject.ParamFlags.READABLE |
                                               GObject.ParamFlags.WRITABLE |
                                               GObject.ParamFlags.CONSTRUCT_ONLY)

    simulator_types: Gio.ListModel = GObject.Property(type=Gio.ListModel)

    @simulator_types.getter  # type: ignore
    def simulator_types(self) -> Gio.ListModel:
        """Returns a list of all available simulator types."""
        # TODO: Get them from the simulator factory singleton
        return Gio.ListStore()

    def __init__(self, context: ModelContext) -> None:
        super().__init__(
            projects=Gtk.MapListModel.new(context.projects, self.__project_map_func),
            result_manager=ResultManager(context.result_manager)
        )

        self.__context = context

    def __project_map_func(self, project: ModelProject) -> Project:
        return Project(project)

    async def load(self) -> None:
        """
        Loads this context. Loads the list of projects, and the result manager.
        """

        await self.__context.load()

    async def create_project(
        self, name: str, sim_type: SimulatorType,
        simulation_file_path: str, project_file_path: str
    ) -> str:
        """
        Creates a new project and returns its id.
        :param name: the name of the new project
        :param sim_type: the simulator type of the new project
        :param simulation_file_path: the simulation file path of the new project
        :param project_file_path: the project file path of the new project
        :return: the id of the newly created project
        """
        return await self.__context.create_project(
            name, sim_type, simulation_file_path, project_file_path
        )

    async def delete_project(self, project_id: str) -> None:
        """
        Deletes the project with the given id.
        :param project_id: the id of the project to delete
        """

        await self.__context.delete_project(project_id)
