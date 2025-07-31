"""This module defines the Context Class"""

from gi.repository import GObject, Gio

import sbaid.common
from sbaid.model.database import global_sqlite
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.model.database.project_sqlite import ProjectSQLite
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.project import Project
from sbaid.model.results.result_manager import ResultManager


class Context(GObject.GObject):
    """This class defines the Context class. The root class that is created at startup.
    Manages the projects and holds a reference to the ResultManager."""

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
        global_db = global_sqlite.get_instance(GlobalSQLite)
        projects: list[tuple[str, SimulatorType, str, str]] = await global_db.get_all_projects()

        for project_id, simulator_type, simulation_file_path, project_file_path in projects:
            project_db = ProjectSQLite(Gio.File.new_for_path(project_file_path))
            project = Project(project_id, simulator_type,
                                         simulation_file_path, project_file_path, project_db)
            self.projects.append(project)
            await project.load_from_db()
        await self.result_manager.load_from_db()

    def create_project(self, name: str, sim_type: SimulatorType, simulation_file_path: str,
                       project_file_path: str) -> str:
        """Creates a new project with the given data and returns the unique ID of the new
        project."""
        project_file = Gio.File.new_for_path(project_file_path)
        project_db_file = project_file.get_child(name + "_db")
        project_db = ProjectSQLite(project_db_file)
        project = Project(name, sim_type, simulation_file_path, project_file_path, project_db)

        self.projects.append(project)

        return self.projects.index(project)

    def delete_project(self, project_id: str) -> None:
        """Deletes the project with the given ID."""
        for project in sbaid.common.list_model_iterator(self.projects):
            if project.id == project_id:
                self.projects.remove(project)
