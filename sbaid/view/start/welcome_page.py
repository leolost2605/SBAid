"""
This module contains the welcome page.
"""
import sys
from typing import Any

import gi

import sbaid.common
from sbaid.view_model.context import Context
from view_model.project import Project

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

        self.create_project = Gtk.Button(label="Create Project")
        self.create_project.set_action_name("win.create-project-page")

        self.all_projects = Gtk.Button(label="All Projects")
        self.all_projects.set_action_name("win.all-projects")

        self.results = Gtk.Button(label="Results")
        self.results.set_action_name("win.results")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # create listmodel containing the latest 3 project
        self.last_projects_box = Gtk.ListBox(name="Last Projects")
        print(self.__context.projects.get_n_items())
        sorted_lm = Gtk.SortListModel.new(self.__context.projects)
        sorted_lm.set_section_sorter(Gtk.CustomSorter.new(self.__sort_name_func))
        print(sorted_lm.get_n_items())
        for project in sbaid.common.list_model_iterator(sorted_lm):
            print(project.name)
        assert sorted_lm is not None
        projects_to_show = Gtk.SliceListModel.new(sorted_lm, 0, 3)
        # TODO sort by last edited DateTime value descending
        self.last_projects_box.bind_model(projects_to_show,
                                          # pylint: disable=unnecessary-lambda
                                          lambda x: self.__create_last_project_button(x))

        box.append(self.create_project)
        box.append(self.last_projects_box)
        box.append(self.all_projects)
        box.append(self.results)

        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)

        main_view.set_content(box)

        self.set_title("Welcome Page")
        self.set_child(main_view)

    def __create_last_project_button(self, proj: Project) -> Gtk.Button:
        button = Gtk.Button()
        button.set_action_name("win.open-project")
        button.set_action_target_value(GLib.Variant.new_string(proj.id))
        proj.bind_property("name", button, "label", GObject.BindingFlags.SYNC_CREATE)
        return button

    def __sort_name_func(self, project1: Any, project2: Any, data: Any) -> int | None:
        if not isinstance(project1, Project) or not isinstance(project2, Project):
            return None
        if project1.name > project2.name:
            return 1
        if project1.name < project2.name:
            return -1
        return 0