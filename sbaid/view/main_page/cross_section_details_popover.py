"""
This module contains the class used to add new cross sections.
"""

import sys

import gi

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.view import utils
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.network.network import Network
from sbaid.view.i18n import i18n

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

    # pylint: disable=too-many-locals,too-many-statements
    def __init__(self, project_id: str, network: Network, cross_section: CrossSection) -> None:
        super().__init__()
        self.__network = network
        self.__cross_section = cross_section

        name_entry = Gtk.Entry()
        cross_section.bind_property("name", name_entry, "text",
                                    GObject.BindingFlags.SYNC_CREATE |
                                    GObject.BindingFlags.BIDIRECTIONAL)

        type_label = Gtk.Label.new("Type:")
        type_label.set_halign(Gtk.Align.END)
        type_value_label = Gtk.Label.new(None)
        type_value_label.set_halign(Gtk.Align.START)
        cross_section.bind_property("type", type_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE,
                                    self.__transform_type)

        lanes_label = Gtk.Label.new("Lanes:")
        lanes_label.set_halign(Gtk.Align.END)
        lanes_value_label = Gtk.Label.new(None)
        lanes_value_label.set_halign(Gtk.Align.START)
        cross_section.bind_property("lanes", lanes_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE)

        hard_shoulder_label = Gtk.Label.new("Hard shoulder:")
        hard_shoulder_label.set_halign(Gtk.Align.END)
        hard_shoulder_value_label = Gtk.Label.new(None)
        hard_shoulder_value_label.set_halign(Gtk.Align.START)
        cross_section.bind_property("hard-shoulder-available", hard_shoulder_value_label, "label",
                                    GObject.BindingFlags.SYNC_CREATE,
                                    self.__transform_hard_shoulder)

        delete_button = Gtk.Button.new_with_label(i18n._("Delete"))
        delete_button.add_css_class("destructive-action")
        delete_button.connect("clicked", self.__on_delete_clicked)

        builder = GLib.VariantBuilder(GLib.VariantType("(ss)"))
        builder.add_value(GLib.Variant.new_string(project_id))
        builder.add_value(GLib.Variant.new_string(cross_section.id))
        target = builder.end()

        edit_button = Gtk.Button.new_with_label(i18n._("Edit"))
        edit_button.set_action_name("win.edit-cross-section")
        edit_button.set_action_target_value(target)

        move_button = Gtk.Button.new_with_label(i18n._("Move"))
        move_button.set_action_name("cross-section.move")
        move_button.set_action_target_value(GLib.Variant.new_string(cross_section.id))

        button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 3)
        button_box.set_halign(Gtk.Align.END)
        button_box.append(delete_button)
        button_box.append(edit_button)
        button_box.append(move_button)

        grid = Gtk.Grid(row_spacing=6, column_spacing=6, column_homogeneous=True)
        grid.attach(name_entry, 0, 0, 2, 1)
        grid.attach(type_label, 0, 1, 1, 1)
        grid.attach(type_value_label, 1, 1, 1, 1)
        grid.attach(lanes_label, 0, 2, 1, 1)
        grid.attach(lanes_value_label, 1, 2, 1, 1)
        grid.attach(hard_shoulder_label, 0, 3, 1, 1)
        grid.attach(hard_shoulder_value_label, 1, 3, 1, 1)
        grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 4, 2, 1)
        grid.attach(button_box, 0, 5, 2, 1)

        self.set_child(grid)

        self.connect("map", lambda widget: edit_button.grab_focus())

    @staticmethod
    def __transform_type(binding: GObject.Binding, type_enum: CrossSectionType) -> str:
        return type_enum.name

    @staticmethod
    def __transform_hard_shoulder(binding: GObject.Binding, available: bool) -> str:
        if available:
            return "Available"
        return "Unavailable"

    def __on_delete_clicked(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(
            self.__network.delete_cross_section(self.__cross_section.id))
