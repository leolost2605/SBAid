"""
This module contains the class used to add new cross sections.
"""

import sys

import gi

from sbaid.common.location import Location
from sbaid.view import utils
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, GObject, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionDetailsPopover(Gtk.Popover):
    """
    Popover used to add new cross sections to the list.
    """

    __network: Network
    __cross_section: CrossSection

    def __init__(self, project_id: str, network: Network, cross_section: CrossSection) -> None:
        super().__init__()
        self.__network = network
        self.__cross_section = cross_section

        name_label = Gtk.Label.new(None)
        cross_section.bind_property("name", name_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE)

        x_label = Gtk.Label.new("X:")
        x_label.set_halign(Gtk.Align.END)
        x_value_label = Gtk.Label.new(None)
        x_value_label.set_halign(Gtk.Align.START)
        cross_section.bind_property("location", x_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE,
                                    self.__transform_location_to_x)

        y_label = Gtk.Label.new("Y:")
        y_label.set_halign(Gtk.Align.END)
        y_value_label = Gtk.Label.new(None)
        y_value_label.set_halign(Gtk.Align.START)
        cross_section.bind_property("location", y_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE,
                                    self.__transform_location_to_y)

        delete_button = Gtk.Button.new_with_label("Delete")
        delete_button.add_css_class("destructive-action")
        delete_button.connect("clicked", self.__on_delete_clicked)

        builder = GLib.VariantBuilder(GLib.VariantType("(ss)"))
        builder.add_value(GLib.Variant.new_string(project_id))
        builder.add_value(GLib.Variant.new_string(cross_section.id))
        target = builder.end()

        edit_button = Gtk.Button.new_with_label("Edit")
        edit_button.set_action_name("win.edit-cross-section")
        edit_button.set_action_target_value(target)

        grid = Gtk.Grid(row_spacing=6, column_spacing=6, column_homogeneous=True)
        grid.attach(name_label, 0, 0, 2, 1)
        grid.attach(x_label, 0, 1, 1, 1)
        grid.attach(x_value_label, 1, 1, 1, 1)
        grid.attach(y_label, 0, 2, 1, 1)
        grid.attach(y_value_label, 1, 2, 1, 1)
        grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 3, 2, 1)
        grid.attach(delete_button, 0, 4, 1, 1)
        grid.attach(edit_button, 1, 4, 1, 1)

        self.set_child(grid)

    @staticmethod
    def __transform_location_to_x(binding: GObject.Binding, loc: Location) -> str:
        return str(loc.x)

    @staticmethod
    def __transform_location_to_y(binding: GObject.Binding, loc: Location) -> str:
        return str(loc.y)

    def __on_delete_clicked(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(
            self.__network.delete_cross_section(self.__cross_section.id))
