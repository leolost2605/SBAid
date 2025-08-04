import sys

import gi

from sbaid.view.main_page.add_new_cross_section_list_popover import AddNewCrossSectionListPopover
from sbaid.view.main_page.network_map import NetworkMap
from sbaid.view_model.network.cross_section import CrossSection

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Project:
    pass


class ProjectMainPage(Adw.NavigationPage):
    __project: Project

    def __init__(self, project: Project) -> None:
        super().__init__()

        self.__project = project

        side_header_bar = Adw.HeaderBar.new()

        cross_sections_list = Gtk.ListBox.new()
        cross_sections_list.bind_model(project.network.cross_sections, self.__create_cs_row)

        scrolled_window = Gtk.ScrolledWindow.new()
        scrolled_window.set_child(cross_sections_list)
        scrolled_window.set_vexpand(True)

        add_cs_button = Gtk.MenuButton.new()
        add_cs_button.set_label("+ Add Cross Section")
        add_cs_button.set_popover(AddNewCrossSectionListPopover(project.network))

        sidebar = Adw.ToolbarView.new()
        sidebar.add_top_bar(side_header_bar)
        sidebar.set_content(scrolled_window)
        sidebar.add_bottom_bar(add_cs_button)

        start_button = Gtk.Button.new_with_label("Start Simulating")
        start_button.set_action_name("win.start-simulation")
        start_button.set_action_target_value(GLib.Variant.new_string(project.id))

        start_menu = Gio.Menu.new()
        start_menu.append("Edit Algorithm Configurations",
                          Gio.Action.print_detailed_name("win.edit-algo-configs",
                                                         GLib.Variant.new_string(project.id)))

        menu_button = Gtk.MenuButton.new()
        menu_button.set_menu_model(start_menu)

        content_header_bar = Adw.HeaderBar.new()
        content_header_bar.pack_end(menu_button)
        content_header_bar.pack_end(start_button)

        network_map = NetworkMap(project.network)

        content = Adw.ToolbarView.new()
        content.add_top_bar(content_header_bar)
        content.set_content(network_map)

        main_view = Adw.OverlaySplitView.new()
        main_view.set_sidebar(sidebar)
        main_view.set_content(content)

        self.set_child(main_view)
        self.set_title(project.name)

    def __create_cs_row(self, cross_section: CrossSection) -> Gtk.Widget:
        label = Gtk.Label.new(None)
        cross_section.bind_property("name", label, "label",
                                    GObject.BindingFlags.SYNC_CREATE)
        return label
