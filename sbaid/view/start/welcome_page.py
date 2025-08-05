"""
This module contains the welcome page.
"""
import asyncio
import sys
from unittest import mock

import gi
from gi.repository.GLib import Variant
from gi.repository.Gtk import Widget

import common
from common.simulator_type import SimulatorType
from view_model.context import Context
from view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GLib, Gio, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class WelcomePage(Adw.NavigationPage):
    """
    This page is the first page displayed when opening sbaid.
    It welcomes the user and provides a list of recently used project as well
    as allowing to view all projects and the result view.
    """

    def __init__(self, context: Context) -> None:
        self.__context = context
        common.run_coro_in_background(
            context.create_project("my_name", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                                   "my_simulator", "my_project_path"))
        common.run_coro_in_background(
            context.create_project("my_name2", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                                   "my_simulator", "my_project_path"))
        common.run_coro_in_background(
            context.create_project("my_name3", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                                   "my_simulator", "my_project_path"))


        print(context.projects.get_n_items())
        super().__init__()

        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)


        self.last_projects_box = Gtk.ListBox(name="Last Projects")
        one_project_button = Gtk.Button()
        context.projects.get_item(0).bind_property("name", one_project_button, "label", GObject.BindingFlags.SYNC_CREATE)
        context.projects.get_item(0).name = "asodgnowaeunawuenb"
        self.last_projects_box.append(one_project_button)
        # self.last_projects_box.bind_model(context.projects,
        #                                   lambda x: self.__create_last_project_button(x))

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.create_project = Gtk.Button(label="Create Project")
        # self.create_project = Adw.ActionRow(title="Create Project")
        self.create_project.set_action_name("win.create-project-page")
        self.create_project.connect("clicked", self._on_create_project)
        # self.last_projects: list[Widget] = []
        # for i, project in enumerate(common.list_model_iterator(context.projects)):
        #     if i > 2: break
        #     proj_button = Gtk.Button(label="test_name_aoewuinvawpoegn")
        #     proj_button.set_action_target_value(
        #         GLib.Variant.new_string(project.name))
        #     proj_button.set_action_name("win.open-project")
        #     proj_button.connect("clicked", self._on_open_project, proj_button)
        #     self.last_projects.append(proj_button)

        #
        # self.last_opened_1 = Gtk.Button(label="Open1")  # TODO maybe turn into adw expander rows
        # self.last_opened_1.set_action_target_value(GLib.Variant.new_string("test_project_1"))  # TODO change project name
        # self.last_opened_1.set_action_name("win.open-project")
        # self.last_opened_1.connect("clicked", self._on_open_project, self.last_opened_1)
        #
        # self.last_opened_2 = Gtk.Button(label="Open2")
        # self.last_opened_2.set_action_target_value(
        #     GLib.Variant.new_string("test_project_2"))  # TODO change project name
        # self.last_opened_2.set_action_name("win.open-project")
        # self.last_opened_2.connect("clicked", self._on_open_project, self.last_opened_1)
        #
        # self.last_opened_3 = Gtk.Button(label="Open3")
        # self.last_opened_3.set_action_target_value(
        #     GLib.Variant.new_string("test_project_3"))  # TODO change project name
        # self.last_opened_3.set_action_name("win.open-project")
        # self.last_opened_3.connect("clicked", self._on_open_project, self.last_opened_1)

        self.all_projects = Gtk.Button(label="All Projects")
        self.all_projects.set_action_name("win.all-projects")
        self.all_projects.connect("clicked", self._on_all_projects)

        self.results = Gtk.Button(label="Results")
        self.results.set_action_name("win.results")
        self.results.connect("clicked", self._on_results)

        box.append(self.create_project)
        box.append(self.last_projects_box)
        box.append(self.all_projects)
        box.append(self.results)

        main_view.set_content(box)

        self.set_child(main_view)
        self.set_title("Welcome Page")

    def _on_create_project(self, widget: Gtk.Widget) -> None:
        # print("debug: ", self.__context.projects.get_item(0).name)
        # print("debug: ", self.__context.projects.get_item(1).name)
        # print("debug: ", self.__context.projects.get_item(2).name)
        # self.__context.projects.get_item(0).name = "EOINSG"
        # self.__context.projects.get_item(1).name = "EOINSG2"
        # self.__context.projects.get_item(2).name = "EOINSG3"
        # self.create_project.activate_action("create_project-page")
        self.__context.projects.get_item(0).name = "different name"

    def _on_open_project(self, widget: Gtk.Widget, proj) -> None:
        self.proj.activate_action("open_project")

    def _on_all_projects(self, widget: Gtk.Widget) -> None:
        self.all_projects.activate_action("all_projects")

    def _on_results(self, widget: Gtk.Widget) -> None:
        self.results.activate_action("results")

    def __create_last_project_button(self, proj: GObject.GObject) -> Gtk.Button:
        button = Gtk.Button()
        print("on widget creation:", proj.name)
        proj.bind_property("name", button, "label", GObject.BindingFlags.SYNC_CREATE)
        # button.set_action_target_value(GLib.Variant.new_string(button.get_label()))
        # button.set_action_name("win.open-project")
        # button.connect("clicked", self._on_open_project, button)
        return button
