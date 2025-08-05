"""
This module contains the welcome page.
"""
import sys
import gi
from gi.overrides.GLib import Variant

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class WelcomePage(Adw.NavigationPage):
    """
    This page is the first page displayed when opening sbaid.
    It welcomes the user and provides a list of recently used project as well
    as allowing to view all projects and the result view.
    """

    def __init__(self) -> None:
        super().__init__()

        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.create_project = Gtk.Button(label="Create Project")
        # self.create_project = Adw.ActionRow(title="Create Project")
        self.create_project.set_action_name("win.create-project-page")
        self.create_project.connect("clicked", self._on_create_project)

        self.last_opened_1 = Gtk.Button(label="Open1")  # TODO maybe turn into adw expander rows
        self.last_opened_1.set_action_target_value(GLib.Variant.new_string("test_project_1"))  # TODO change project name
        self.last_opened_1.set_action_name("win.open-project")
        self.last_opened_1.connect("clicked", self._on_open_project, self.last_opened_1)

        self.last_opened_2 = Gtk.Button(label="Open2")
        self.last_opened_2.set_action_target_value(
            GLib.Variant.new_string("test_project_2"))  # TODO change project name
        self.last_opened_2.set_action_name("win.open-project")
        self.last_opened_2.connect("clicked", self._on_open_project, self.last_opened_1)

        self.last_opened_3 = Gtk.Button(label="Open3")
        self.last_opened_3.set_action_target_value(
            GLib.Variant.new_string("test_project_3"))  # TODO change project name
        self.last_opened_3.set_action_name("win.open-project")
        self.last_opened_3.connect("clicked", self._on_open_project, self.last_opened_1)

        self.all_projects = Gtk.Button(label="All Projects")
        self.all_projects.set_action_name("win.all-projects")
        self.all_projects.connect("clicked", self._on_all_projects)

        self.results = Gtk.Button(label="Results")
        self.results.set_action_name("win.results")
        self.all_projects.connect("clicked", self._on_results)

        box.append(self.create_project)
        box.append(self.last_opened_1)
        box.append(self.last_opened_2)
        box.append(self.last_opened_3)
        box.append(self.all_projects)
        box.append(self.results)

        main_view.set_content(box)

        self.set_child(main_view)
        self.set_title("Welcome Page")

    def _on_create_project(self, widget: Gtk.Widget) -> None:
        self.create_project.activate_action("create_project-page")

    def _on_open_project(self, widget: Gtk.Widget, proj) -> None:
        self.proj.activate_action("open_project")

    def _on_all_projects(self, widget: Gtk.Widget) -> None:
        self.last_opened_1.activate_action("all_projects")

    def _on_results(self, widget: Gtk.Widget) -> None:
        self.last_opened_1.activate_action("results")

