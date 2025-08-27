"""
This module contains the project main page.
"""

from typing import cast
import sys

import gi

from sbaid.view import utils
from sbaid.view.main_page.add_new_cross_section_list_popover import AddNewCrossSectionListPopover
from sbaid.view.main_page.network_map import NetworkMap
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.project import Project
from sbaid.view.i18n import i18n

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ProjectMainPage(Adw.NavigationPage):
    """
    This class represents the main page where the project is opened to.
    It contains the network map and lists all cross sections in the sidebar.
    It also allows to open the edit algorithm configurations dialog and start a simulation.
    """

    __project: Project
    __network_map: NetworkMap

    def __init__(self, project: Project) -> None:
        super().__init__()

        self.__project = project

        self.__placeholder = Adw.StatusPage(title=i18n._("Loading..."))

        placeholder_view = Adw.ToolbarView(content=self.__placeholder)
        placeholder_view.add_top_bar(Adw.HeaderBar())

        start_button = Gtk.Button.new_with_label(i18n._("Start Simulating"))
        start_button.add_css_class("suggested-action")
        start_button.set_action_name("win.run-simulation")
        start_button.set_action_target_value(GLib.Variant.new_string(project.id))

        start_menu = Gio.Menu()
        start_menu.append(i18n._("Edit Algorithm Configurations"),
                          Gio.Action.print_detailed_name("win.edit-algo-configs",
                                                         GLib.Variant.new_string(project.id)))

        menu_button = Gtk.MenuButton()
        menu_button.set_menu_model(start_menu)

        start_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        start_box.add_css_class("linked")
        start_box.append(start_button)
        start_box.append(menu_button)

        header_bar = Adw.HeaderBar()
        header_bar.pack_end(start_box)

        cross_sections_list = Gtk.ListBox()
        cross_sections_list.set_css_classes([])
        cross_sections_list.bind_model(project.network.cross_sections, self.__create_cs_row)
        cross_sections_list.connect("row-activated", self.__on_cs_row_activated)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(cross_sections_list)
        scrolled_window.set_vexpand(True)

        add_cs_button = Gtk.MenuButton(direction=Gtk.ArrowType.UP)
        add_cs_button.set_label("+ " + i18n._("Add Cross Section"))
        add_cs_button.set_popover(AddNewCrossSectionListPopover(project.network))

        sidebar = Adw.ToolbarView()
        sidebar.set_content(scrolled_window)
        sidebar.add_bottom_bar(add_cs_button)

        self.__network_map = NetworkMap(project.id, project.network)

        split_view = Adw.OverlaySplitView()
        split_view.set_sidebar(sidebar)
        split_view.set_content(self.__network_map)

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(split_view)

        self.__stack = Gtk.Stack()
        self.__stack.add_child(placeholder_view)
        self.__stack.add_named(main_view, "main-view")

        self.set_child(self.__stack)
        self.set_title(project.name)

        utils.run_coro_with_error_reporting(self.__load())

    def __create_cs_row(self, cross_section: CrossSection) -> Gtk.Widget:
        label = Gtk.Label(xalign=0, margin_top=6, margin_bottom=6, margin_end=12, margin_start=6)
        cross_section.bind_property("name", label, "label",
                                    GObject.BindingFlags.SYNC_CREATE)
        return label

    def __on_cs_row_activated(self, list_box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        index = row.get_index()
        cross_section = cast(CrossSection, self.__project.network.cross_sections.get_item(index))
        self.__network_map.show_cross_section_details(cross_section)

    async def __load(self) -> None:
        try:
            await self.__project.load()
            self.__stack.set_visible_child_name("main-view")
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.__placeholder.set_title(i18n._("Failed to load project"))
            self.__placeholder.set_description(str(e))
