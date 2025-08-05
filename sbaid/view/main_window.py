"""
This module contains the main window of sbaid.
"""

import sys
from typing import Any, cast

import gi

from sbaid import common
from sbaid.view.main_page.project_main_page import ProjectMainPage
from sbaid.view_model.context import Context
from sbaid.view_model.project import Project
from sbaid.view.start.welcome_page import WelcomePage

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ProjectNotFoundError(Exception):
    """Raised when an action was activated with a project id that doesn't exist."""


class CrossSectionNotFoundError(Exception):
    """Raised when an action was activated with a cross section id that doesn't exist."""


class MainWindow(Adw.ApplicationWindow):
    """
    This class contains the main window of the application.
    It handles managing the pages and provides actions for opening new ones.
    """
    __context: Context
    __nav_view: Adw.NavigationView

    def __init__(self, context: Context, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.__context = context

        welcome_page = WelcomePage()

        self.__nav_view = Adw.NavigationView()
        self.__nav_view.add(welcome_page)

        self.set_content(self.__nav_view)

        # Add actions
        open_project_action = Gio.SimpleAction.new("open-project", GLib.VariantType.new("s"))
        open_project_action.connect("activate", self.__on_open_project)

        edit_algo_configs_action = Gio.SimpleAction.new("edit-algo-configs",
                                                        GLib.VariantType.new("s"))
        edit_algo_configs_action.connect("activate", self.__on_edit_algo_configs)

        edit_cross_section_action = Gio.SimpleAction.new("edit-cross-section",
                                                         GLib.VariantType.new("(ss)"))
        edit_cross_section_action.connect("activate", self.__on_edit_cross_section)

        run_simulation_action = Gio.SimpleAction.new("run-simulation", GLib.VariantType.new("s"))
        run_simulation_action.connect("activate", self.__on_run_simulation)

        self.add_action(open_project_action)
        self.add_action(edit_algo_configs_action)
        self.add_action(edit_cross_section_action)
        self.add_action(run_simulation_action)

    def __get_project_by_id(self, project_id: str) -> Project:
        for project in common.list_model_iterator(self.__context.projects):
            if project.id == project_id:
                return cast(Project, project)

        raise ProjectNotFoundError(f"The project with the id {project_id} was not found.")

    def __on_open_project(self, action: Gio.SimpleAction, param: GLib.Variant) -> None:
        project = self.__get_project_by_id(param.get_string())
        self.__nav_view.push(ProjectMainPage(project))

    def __on_edit_algo_configs(self, action: Gio.SimpleAction, param: GLib.Variant) -> None:
        project = self.__get_project_by_id(param.get_string())
        # pylint: disable=undefined-variable
        self.__nav_view.push(ParameterEditingPage(  # type: ignore # noqa
            project.algorithm_configuration_manager))

    def __on_edit_cross_section(self, action: Gio.SimpleAction, param: GLib.Variant) -> None:
        project_id = param.get_child_value(0).get_string()
        cross_section_id = param.get_child_value(1).get_string()
        project = self.__get_project_by_id(project_id)

        for cs in common.list_model_iterator(project.network.cross_sections):
            if cs.id == cross_section_id:
                # pylint: disable=undefined-variable
                self.__nav_view.push(CrossSectionEditingPage(  # type: ignore # noqa
                    project.algorithm_configuration_manager))
                return

        raise CrossSectionNotFoundError(f"The cross_section with the id {cross_section_id} "
                                        "was not found.")

    def __on_run_simulation(self, action: Gio.SimpleAction, param: GLib.Variant) -> None:
        project = self.__get_project_by_id(param.get_string())
        # pylint: disable=undefined-variable
        self.__nav_view.push(SimulationRunningPage(project))  # type: ignore # noqa
