"""This module defines the Context Class"""
from gi.repository import GObject, Gio, GLib
from sbaid import common
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.project import Project
from sbaid.model.results.result_manager import ResultManager


class ProjectNotFoundError(Exception):
    """Raised when a project couldn't be found."""


class Context(GObject.GObject):
    """This class defines the Context class. The root class that is created at startup.
    Manages the projects and holds a reference to the ResultManager."""

    __global_db: GlobalDatabase
    __projects: Gio.ListStore

    result_manager: ResultManager = GObject.Property(type=ResultManager,  # type: ignore
                                                     flags=GObject.ParamFlags.READABLE |
                                                     GObject.ParamFlags.WRITABLE |
                                                     GObject.ParamFlags.CONSTRUCT_ONLY)
    projects: Gio.ListModel = GObject.Property(type=Gio.ListModel,  # type: ignore
                                               flags=GObject.ParamFlags.READABLE)

    @projects.getter  # type: ignore
    def projects(self) -> Gio.ListModel:
        """Returns the list with all projects"""
        return self.__projects

    def __init__(self) -> None:
        # pylint: disable=no-value-for-parameter
        db_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])
        self.__global_db = GlobalSQLite(db_file)
        super().__init__(result_manager=ResultManager(self.__global_db))
        self.__projects = Gio.ListStore.new(Project)

    def close(self) -> None:
        """Closes the Context."""
        self.__global_db.close()

    async def load(self) -> None:
        """Loads the projects and the results."""
        await self.__global_db.open()

        projects = await self.__global_db.get_all_projects()
        for project_id, simulator_type, simulation_file_path, project_file_path in projects:
            project = Project(project_id, simulator_type,
                              simulation_file_path, project_file_path, self.result_manager)
            await project.load_from_db()
            self.__projects.append(project)

        await self.result_manager.load_from_db()

    async def create_project(self, name: str, sim_type: SimulatorType, simulation_file_path: str,
                             project_file_path: str) -> str:
        """Creates a new project with the given data and returns the unique ID of the new
        project."""

        project_id = GLib.uuid_string_random()  # pylint: disable=no-value-for-parameter

        await self.__global_db.add_project(project_id, sim_type, simulation_file_path,
                                           project_file_path)
        new_project = Project(project_id, sim_type, simulation_file_path,
                              project_file_path, self.result_manager)

        await new_project.load_from_db()

        new_project.name = name

        self.__projects.append(new_project)

        return project_id

    async def delete_project(self, project_id: str) -> None:
        """Deletes the project with the given ID."""
        for pos, project in enumerate(common.list_model_iterator(self.__projects)):
            if project.id == project_id:
                self.__projects.remove(pos)
                await self.__global_db.remove_project(project_id)
                await project.delete()
                return

        raise ProjectNotFoundError(f"The Project with the id {project_id} was not found")
