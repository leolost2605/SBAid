"""
This module contains the class used to add new cross sections.
"""

import sys

import gi

from sbaid import common
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AddNewCrossSectionListPopover(Gtk.Popover):
    """
    Popover used to add new cross sections to the list.
    """

    __network: Network
    __name_entry: Gtk.Entry
    __x_entry: Gtk.Entry
    __y_entry: Gtk.Entry
    __type_drop_down: Gtk.DropDown

    def __init__(self, network: Network) -> None:
        super().__init__()
        self.__network = network

        name_label = Gtk.Label.new("Name:")
        name_entry = Gtk.Entry.new()
        self.__name_entry = name_entry

        x_label = Gtk.Label.new("X:")
        x_entry = Gtk.Entry.new()
        self.__x_entry = x_entry

        y_label = Gtk.Label.new("Y:")
        y_entry = Gtk.Entry.new()
        self.__y_entry = y_entry

        cs_types = ["Display", "Measuring", "Combined"]
        type_drop_down = Gtk.DropDown.new_from_strings(cs_types)
        self.__type_drop_down = type_drop_down

        done_button = Gtk.Button.new_with_label("Add")
        done_button.connect("clicked", self.__on_done_clicked)

        grid = Gtk.Grid.new()
        grid.attach(name_label, 0, 0, 1, 1)
        grid.attach(name_entry, 1, 0, 3, 1)
        grid.attach(x_label, 0, 1, 1, 1)
        grid.attach(x_entry, 1, 1, 1, 1)
        grid.attach(y_label, 2, 1, 1, 1)
        grid.attach(y_entry, 3, 1, 1, 1)
        grid.attach(type_drop_down, 0, 2, 4, 1)
        grid.attach(done_button, 4, 3, 1, 1)

        self.set_child(grid)

    def __on_done_clicked(self, button: Gtk.Button) -> None:
        common.run_coro_in_background(self.__add_cross_section())
        self.popdown()

    async def __add_cross_section(self) -> None:
        name = self.__name_entry.get_text()
        # TODO: Check valid
        x = float(self.__x_entry.get_text())
        y = float(self.__y_entry.get_text())
        location = Location(x, y)
        cs_type = CrossSectionType.DISPLAY
        match self.__type_drop_down.get_selected():
            case 0:
                cs_type = CrossSectionType.DISPLAY

            case 1:
                cs_type = CrossSectionType.MEASURING

            case 2:
                cs_type = CrossSectionType.COMBINED

        await self.__network.create_cross_section(name, location, cs_type)
        # TODO: Select pos
