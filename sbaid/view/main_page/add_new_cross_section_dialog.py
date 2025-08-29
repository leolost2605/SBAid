"""
This module contains the class used to add new cross sections.
"""

import sys
from typing import cast

import gi

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.view import utils
from sbaid.view.i18n import i18n
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AddNewCrossSectionDialog(Adw.Dialog):
    """
    Dialog used to add new cross sections to the simulation.
    """

    __network: Network

    def __init__(self, network: Network, x: float | None = None, y: float | None = None) -> None:
        super().__init__()
        self.__network = network

        header_bar = Adw.HeaderBar()

        self.__name_row = Adw.EntryRow(title=i18n._("Name"))

        self.__x_row = Adw.SpinRow.new_with_range(-180, 180, 0.5)
        self.__x_row.set_value(0)
        self.__x_row.set_title("X")
        self.__x_row.set_digits(6)

        if x is not None:
            self.__x_row.set_value(x)

        self.__y_row = Adw.SpinRow.new_with_range(-90, 90, 0.5)
        self.__y_row.set_value(0)
        self.__y_row.set_title("Y")
        self.__y_row.set_digits(6)

        if y is not None:
            self.__y_row.set_value(y)

        types = Adw.EnumListModel.new(CrossSectionType)
        expression = Gtk.PropertyExpression.new(Adw.EnumListItem, None, "name")
        self.__type_row = Adw.ComboRow(model=types, title="Type", expression=expression)

        group = Adw.PreferencesGroup(margin_start=6, margin_end=6,
                                     margin_top=6, margin_bottom=6)
        group.add(self.__name_row)
        group.add(self.__x_row)
        group.add(self.__y_row)
        group.add(self.__type_row)

        done_button = Gtk.Button.new_with_label(i18n._("Add"))
        done_button.set_margin_end(6)
        done_button.set_margin_bottom(6)
        done_button.set_halign(Gtk.Align.END)
        done_button.add_css_class("suggested-action")
        done_button.connect("clicked", self.__on_done_clicked)

        toolbar_view = Adw.ToolbarView(content=group)
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.add_bottom_bar(done_button)

        self.set_child(toolbar_view)
        self.set_title(i18n._("Add Cross Section"))
        self.set_content_width(500)

    def __on_done_clicked(self, button: Gtk.Button) -> None:
        self.close()
        utils.run_coro_with_error_reporting(self.__add_cross_section())

    async def __add_cross_section(self) -> None:
        name = self.__name_row.get_text()
        x = self.__x_row.get_value()
        y = self.__y_row.get_value()
        location = Location(x, y)
        cs_type = cast(CrossSectionType, self.__type_row.get_selected())
        await self.__network.create_cross_section(name, location, cs_type)
