"""
This module contains the welcome page.
"""
import sys
from typing import Any

import gi

from sbaid.view_model.context import Context
from sbaid.view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GLib, GObject
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
        super().__init__()
        self.__context = context

        header_bar = Adw.HeaderBar()

        self.__create_project_button = Gtk.Button(label="Create Project")
        self.__create_project_button.set_action_name("win.create-project-page")

        time_sorter = Gtk.CustomSorter.new(self.__sort_func)
        sort_model = Gtk.SortListModel.new(self.__context.projects, time_sorter)

        recent_projects_slice = Gtk.SliceListModel.new(sort_model, 0, 3)

        self.__last_projects_box = Gtk.ListBox()
        self.__last_projects_box.bind_model(
            recent_projects_slice, self.__create_last_project_button)

        self.__all_projects_button = Gtk.Button(label="All Projects")
        self.__all_projects_button.set_action_name("win.all-projects")

        self.__results_button = Gtk.Button(label="Results")
        self.__results_button.set_action_name("win.results")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, valign=Gtk.Align.CENTER,
                      halign=Gtk.Align.CENTER)
        box.append(self.__create_project_button)
        box.append(self.__last_projects_box)
        box.append(self.__all_projects_button)
        box.append(self.__results_button)

        status_page = Adw.StatusPage(child=box)

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(status_page)

        self.set_title("SBAid")
        self.set_child(main_view)

    def __sort_func(self, project_one: Project, project_two: Project, data: Any) -> int:
        return project_two.last_opened.compare(project_one.last_opened)

    def __create_last_project_button(self, proj: Project) -> Gtk.Button:
        button = Gtk.Button()
        button.set_action_name("win.open-project")
        button.set_action_target_value(GLib.Variant.new_string(proj.id))
        proj.bind_property("name", button, "label", GObject.BindingFlags.SYNC_CREATE)
        return button
