"""
This module contains the welcome page.
"""
import sys
from typing import Any, Callable
import gi
import sbaid.view.i18n as i18n
from sbaid.view_model.context import Context
from sbaid.view_model.project import Project
from sbaid.view.i18n import LanguageWrapper

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GLib, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class WelcomePage(Adw.NavigationPage):  # pylint:disable=too-many-instance-attributes
    """
    This page is the first page displayed when opening sbaid.
    It welcomes the user and provides a list of recently used project as well
    as allowing to view all projects and the result view.
    """
    __language_selection: Gtk.DropDown | None = None
    __gsignals__ = {
        'language_changed': (GObject.SIGNAL_RUN_LAST, None, ())
    }

    def __init__(self, context: Context) -> None:
        from sbaid.view.i18n import _
        print(_)
        super().__init__()
        self.__context = context
        header_bar = Adw.HeaderBar()

        self.__handle_language_dropdown()
        header_bar.pack_start(self.__language_selection)

        self.__create_project_button = Gtk.Button(label=_("Create Project"))
        self.__create_project_button.set_action_name("win.create-project-page")

        self.__time_sorter = Gtk.CustomSorter.new(self.__sort_func)
        sort_model = Gtk.SortListModel.new(self.__context.projects, self.__time_sorter)

        recent_projects_slice = Gtk.SliceListModel.new(sort_model, 0, 3)

        self.__last_projects_box = Gtk.ListBox()
        self.__last_projects_box.add_css_class("background")
        self.__last_projects_box.set_placeholder(Gtk.Label.new("No recently opened projects"))
        self.__last_projects_box.bind_model(
            recent_projects_slice, self.__create_last_project_button)

        self.__all_projects_button = Gtk.Button(label=_("All Projects"))
        self.__all_projects_button.set_action_name("win.all-projects")

        self.__results_button = Gtk.Button(label=_("Results"))
        self.__results_button.set_action_name("win.results")


        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, valign=Gtk.Align.CENTER,
                      halign=Gtk.Align.CENTER)
        box.append(self.__create_project_button)
        box.append(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))
        box.append(self.__last_projects_box)
        box.append(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL))
        box.append(self.__all_projects_button)
        box.append(self.__results_button)

        status_page = Adw.StatusPage(child=box)

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(status_page)

        self.set_title("SBAid")
        self.set_child(main_view)
        self.connect("map", self.__on_map)

    def __sort_func(self, project_one: Project, project_two: Project, data: Any) -> int:
        return project_two.last_opened.compare(project_one.last_opened)

    def __create_last_project_button(self, proj: Project) -> Gtk.ListBoxRow:
        button = Gtk.Button()
        button.set_action_name("win.open-project")
        button.set_action_target_value(GLib.Variant.new_string(proj.id))
        proj.bind_property("name", button, "label", GObject.BindingFlags.SYNC_CREATE)
        return Gtk.ListBoxRow(child=button, focusable=False)

    def __on_map(self, widget: Gtk.Widget) -> None:
        self.__time_sorter.changed(Gtk.SorterChange.DIFFERENT)

    def __on_language_changed(self, selection: Gtk.SingleSelection,
                              pspec: GObject.ParamSpec) -> None:
        self.emit("language_changed")
        item = self.__language_selection.get_selected_item()
        assert isinstance(item, Gtk.StringObject)
        print(item.get_string())
        i18n.i18n.set_active_language(item.get_string())
        self.__init__(self.__context)

    def __handle_language_dropdown(self):
        """todo"""
        if self.__language_selection is None:
            self.__language_selection = Gtk.DropDown.new_from_strings(["en", "de"])
            self.__language_selection.connect("notify::selected-item", self.__on_language_changed)
        else:
            self.__language_selection.unparent()

    def do_language_changed(self) -> None:
        """todo"""
        print("do language changed signal is working")
