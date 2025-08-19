"""
This module contains the class used for representing a cross section in the map.
"""

import sys

import gi

from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.network.network import Network
from sbaid.view.main_page.cross_section_details_popover import CrossSectionDetailsPopover

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionMarker(Adw.Bin):
    """
    Used to represent a cross section on the map.
    """
    __project_id: str
    __network: Network
    __cross_section: CrossSection
    __popover: Gtk.Popover | None = None

    @property
    def cross_section(self) -> CrossSection:
        """Returns the cross section that this marker represents."""
        return self.__cross_section

    def __init__(self, project_id: str, network: Network, cross_section: CrossSection) -> None:
        super().__init__()

        self.__project_id = project_id
        self.__network = network
        self.__cross_section = cross_section

        self.__image = Gtk.Image.new_from_icon_name("location-services-active")
        self.__image.set_icon_size(Gtk.IconSize.LARGE)

        bottom_widget = Adw.Bin()

        size_group = Gtk.SizeGroup.new(Gtk.SizeGroupMode.BOTH)
        size_group.add_widget(self.__image)
        size_group.add_widget(bottom_widget)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        box.append(self.__image)
        box.append(bottom_widget)

        self.set_child(box)

        click = Gtk.GestureClick()
        click.connect("released", self.__on_clicked)
        self.add_controller(click)

    def show_details(self) -> None:
        """
        Opens a popover at this location showing details of the cross section.
        """
        if self.__popover is None:
            self.__popover = CrossSectionDetailsPopover(self.__project_id, self.__network,
                                                        self.__cross_section)
            self.__popover.set_parent(self.__image)

        self.__popover.popup()

    def __on_clicked(self, click: Gtk.GestureClick, n_press: int, x: float, y: float) -> None:
        self.show_details()
