"""This module defines the Context Class"""

from gi.events import GLibEventLoopPolicy
from gi.repository import GObject, Gio, GLib

import sbaid.common
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.project import Project
from sbaid.model.results.result_manager import ResultManager


class Context(GObject.GObject):
    """This class defines the Context class. The root class that is created at startup.
    Manages the projects and holds a reference to the ResultManager."""

    __global_db: GlobalDatabase

    __result_manager: ResultManager
    __projects: Gio.ListModel

    __result_id_pos_map: dict[str, int]


    @GObject.Property(type=ResultManager, flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    def result_manager(self):
        return self.__result_manager

    @GObject.Property(type=Gio.ListModel, flags=GObject.ParamFlags.READABLE |
                                                GObject.ParamFlags.WRITABLE |
                                                GObject.ParamFlags.CONSTRUCT_ONLY)
    def projects(self):
        return self.__projects

    def __init__(self) -> None:
        self.__result_manager = ResultManager()
        self.__projects = Gio.ListStore.new(Project)
        self.__result_id_pos_map = {}
        super().__init__()

    async def load(self) -> None:
        """Loads the projects and the results."""
        self.__global_db = GlobalSQLite(Gio.File.new_for_path("global_db"))
        async with self.__global_db as db:
            projects: list[tuple[str, SimulatorType, str, str]] = \
                await db.get_all_projects()
        for project_id, simulator_type, simulation_file_path, project_file_path in projects:
            project = Project(project_id, simulator_type,
                              simulation_file_path, project_file_path)
            self.projects.append(project)
            self.__result_id_pos_map[project_id] = self.projects.find(project)
            await project.load_from_db()
        await self.result_manager.load_from_db()

    async def create_project(self, sim_type: SimulatorType, simulation_file_path: str,
                       project_file_path: str) -> str:
        """Creates a new project with the given data and returns the unique ID of the new
        project."""

        project_id = GLib.uuid_string_random()  # pylint: disable=no-value-for-parameter

        await self.__project_creation_db_action(project_id, sim_type, simulation_file_path,
                                                project_file_path)

        new_project = Project(project_id, sim_type, simulation_file_path,
                                     project_file_path)
        self.projects.append(new_project)
        self.__result_id_pos_map[project_id] = self.projects.find(new_project)[1]

        return project_id

    async def __project_creation_db_action(self, project_id: str, sim_type: SimulatorType,
                                           simulation_file_path: str,
                                           project_file_path: str) -> None:
        async with self.__global_db as db:
            await db.add_project(project_id, sim_type, simulation_file_path, project_file_path)

    async def delete_project(self, project_id: str) -> None:
        """Deletes the project with the given ID."""
        self.projects.remove(self.__result_id_pos_map[project_id])
        await self.__project_deletion_db_action(project_id)

    async def __project_deletion_db_action(self, project_id: str) -> None:
        async with self.__global_db as db:
            await db.remove_project(project_id)
