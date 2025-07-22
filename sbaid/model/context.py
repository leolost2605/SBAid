"""This module defines the Context Class"""
from typing import List, Tuple
from gi.repository import GObject, Gio, Gtk, Glib
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager
from sbaid.model.database.global_database import GlobalDatabase
from sbaid.model.database.project_database import ProjectDatabase
from sbaid.model.network.network import Network
from sbaid.model.project import Project
from sbaid.model.results.result import Result
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.simulator.simulator import Simulator


class Context(GObject.GObject):
    """This class defines the Context class."""

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

    def load(self) -> None:
        """todo"""
        self.projects = Gtk.ListModel()
        GlobalDatabase.open()  # todo
        projects: List[Tuple[int, str, str, str]] = GlobalDatabase.get_all_projects()
        for project_id, project_type, simulation_file_path, project_file_path in projects:
            project = Project(project_id, project_type, simulation_file_path, project_file_path)
            project.simulator = Simulator(simulation_file_path)
            project.network = Network(project.simulator)
            project.network.cross_sections = Gtk.MapListModel()
            project.algorithm_configuration_manager = AlgorithmConfigurationManager(project.network)
            project.algorithm_configuration_manager.algorithm_configurations = Gtk.ListModel()
            self.projects.append(project)

            project.load_from_db()

            # todo open(file.new_build_file_name(path, 'db')) ???

            project_name = ProjectDatabase.get_project_name()
            last_modified_at = ProjectDatabase.get_last_modified()

        result_manager = ResultManager()
        result_manager.results = Gtk.ListModel()
        result_manager.load_from_db()
        result_manager.available_tags = GlobalDatabase.get_all_tags()
        results = GlobalDatabase.get_all_results()

        for id, date in results:
            result = Result(id, date)
            result.load_from_db()
            result.name = GlobalDatabase.get_result_name()
            result.selected_tags = GlobalDatabase.get_all_tags()
            result_manager.results.append(result)

    def create_project(self, name: str, sim_type: SimulatorType, simulation_file_path: str,
                       project_file_path: str) -> str:
        """todo"""
        project = Project(name, sim_type, simulation_file_path, project_file_path)
        project.simulator = Simulator()
        project.network = Network(project.simulator)
        project.network.cross_sections = Gtk.MapListModel()
        project.algorithm_configuration_manager = AlgorithmConfigurationManager(project.network)
        project.algorithm_configuration_manager.algorithm_configurations = Gio.ListModel()

        self.projects.append(project)

        return self.projects.index(project)

    def delete_project(self, project_id: str) -> None:
        """todo"""
        project_model = self.projects[project_id]
        self.projects.remove(project_model)
        project_model.delete()
