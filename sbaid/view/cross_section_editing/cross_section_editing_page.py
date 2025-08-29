"""
This module contains the cross section editing page.
"""

import sys

import gi

from sbaid.common.location import Location
from sbaid.view import utils
from sbaid.common.i18n import i18n
from sbaid.view_model.network.network import Network
from sbaid.view_model.network.cross_section import CrossSection

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionEditingPage(Adw.NavigationPage):
    """
    This page allows to edit cross sections.
    """

    __cross_section: CrossSection
    __network: Network
    __x_entry: Gtk.Entry
    __y_entry: Gtk.Entry

    # pylint: disable=too-many-locals
    def __init__(self, cross_section: CrossSection, network: Network):
        super().__init__()

        self.__cross_section = cross_section
        self.__network = network

        header_bar = Adw.HeaderBar()

        lanes_label = Gtk.Label.new(i18n._("Lanes:"))

        lanes_value_label = Gtk.Label(halign=Gtk.Align.START)
        cross_section.bind_property("lanes", lanes_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE)

        hard_shoulder_available_label = Gtk.Label.new(i18n._("Rightmost lane is hard shoulder:"))

        hard_shoulder_available_value_label = Gtk.Label(halign=Gtk.Align.START)
        cross_section.bind_property("hard-shoulder-available",
                                    hard_shoulder_available_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE)

        hard_shoulder_active_label = Gtk.Label.new(i18n._("Hard shoulder openable:"))

        hard_shoulder_active_switch = Gtk.Switch(halign=Gtk.Align.START, valign=Gtk.Align.CENTER)
        hard_shoulder_active_switch.bind_property("state", hard_shoulder_active_switch, "active")
        cross_section.bind_property("hard-shoulder-available", hard_shoulder_active_switch,
                                    "sensitive", GObject.BindingFlags.SYNC_CREATE)
        cross_section.bind_property("hard-shoulder-usable", hard_shoulder_active_switch,
                                    "state", GObject.BindingFlags.SYNC_CREATE |
                                    GObject.BindingFlags.BIDIRECTIONAL)

        b_display_active_label = Gtk.Label.new(i18n._("B Display usable:"))

        b_display_active_switch = Gtk.Switch(halign=Gtk.Align.START, valign=Gtk.Align.CENTER)
        b_display_active_switch.bind_property("state", b_display_active_switch, "active")
        cross_section.bind_property("b-display-usable", b_display_active_switch,
                                    "state", GObject.BindingFlags.SYNC_CREATE |
                                    GObject.BindingFlags.BIDIRECTIONAL)

        x_label = Gtk.Label.new("X:")

        self.__x_entry = x_entry = Gtk.Entry()
        cross_section.bind_property("location", x_entry, "text",
                                    GObject.BindingFlags.SYNC_CREATE,
                                    self.__transform_location_to_x)

        y_label = Gtk.Label.new("Y:")

        self.__y_entry = y_entry = Gtk.Entry()
        cross_section.bind_property("location", y_entry, "text",
                                    GObject.BindingFlags.SYNC_CREATE,
                                    self.__transform_location_to_y)

        move_button = Gtk.Button.new_with_label(i18n._("Move"))
        move_button.connect("clicked", self.__on_move)

        move_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 3)
        move_box.append(x_label)
        move_box.append(x_entry)
        move_box.append(y_label)
        move_box.append(y_entry)
        move_box.append(move_button)

        grid = Gtk.Grid(margin_start=12, margin_end=12, margin_top=12, margin_bottom=12,
                        column_spacing=3, row_spacing=6, halign=Gtk.Align.CENTER,
                        valign=Gtk.Align.CENTER)
        grid.attach(lanes_label, 0, 0, 1, 1)
        grid.attach(lanes_value_label, 1, 0, 1, 1)
        grid.attach(hard_shoulder_available_label, 0, 1, 1, 1)
        grid.attach(hard_shoulder_available_value_label, 1, 1, 1, 1)
        grid.attach(hard_shoulder_active_label, 0, 2, 1, 1)
        grid.attach(hard_shoulder_active_switch, 1, 2, 1, 1)
        grid.attach(b_display_active_label, 0, 3, 1, 1)
        grid.attach(b_display_active_switch, 1, 3, 1, 1)
        grid.attach(move_box, 0, 4, 2, 1)

        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.set_content(grid)

        self.set_child(toolbar_view)
        self.set_title(cross_section.name)

    def __on_move(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(self.__move_cs())

    async def __move_cs(self) -> None:
        new_x = float(self.__x_entry.get_text())
        new_y = float(self.__y_entry.get_text())
        new_location = Location(new_x, new_y)
        await self.__network.move_cross_section(self.__cross_section.id, new_location)

    @staticmethod
    def __transform_location_to_x(binding: GObject.Binding, loc: Location) -> str:
        return str(loc.x)

    @staticmethod
    def __transform_location_to_y(binding: GObject.Binding, loc: Location) -> str:
        return str(loc.y)
