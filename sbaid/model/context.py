"""This module defines the Context Class"""
import asyncio

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

    result_manager = GObject.Property(
        type=ResultManager,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    projects = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self) -> None:
        result_manager = ResultManager()
        projects = Gio.ListStore.new(Project)
        super().__init__(result_manager=result_manager, projects=projects)

    async def load(self) -> None:
        """Loads the projects and the results."""
        self.__global_db = GlobalSQLite(Gio.File.new_for_path("global"))
        projects: list[tuple[str, SimulatorType, str, str]] = \
            await self.__global_db.get_all_projects()

        for project_id, simulator_type, simulation_file_path, project_file_path in projects:
            project = Project(project_id, simulator_type,
                              simulation_file_path, project_file_path)
            self.projects.append(project)
            await project.load_from_db()
        await self.result_manager.load_from_db()

    def create_project(self, name: str, sim_type: SimulatorType, simulation_file_path: str,
                       project_file_path: str) -> str:
        """Creates a new project with the given data and returns the unique ID of the new
        project."""

        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        project_id = GLib.uuid_string_random()  # pylint: disable=no-value-for-parameter

        task = loop.create_task(self.__project_creation_db_action(project_id, sim_type,
                                simulation_file_path, project_file_path))
        loop.run_until_complete(task)

        self.projects.append(Project(name, sim_type, simulation_file_path, project_file_path))

        return project_id

    async def __project_creation_db_action(self, project_id: str, sim_type: SimulatorType,
                                           simulation_file_path: str,
                                           project_file_path: str) -> None:
        async with self.__global_db as db:
            await db.add_project(project_id, sim_type, simulation_file_path, project_file_path)

    def delete_project(self, project_id: str) -> None:
        """Deletes the project with the given ID."""
        for project in sbaid.common.list_model_iterator(self.projects):
            if project.id == project_id:
                self.projects.remove(project)

        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()

        task = loop.create_task(self.__project_deletion_db_action(project_id))
        loop.run_until_complete(task)

    async def __project_deletion_db_action(self, project_id: str) -> None:
        async with self.__global_db as db:
            await db.remove_project(project_id)
