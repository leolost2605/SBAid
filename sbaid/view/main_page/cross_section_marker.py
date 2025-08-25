"""
This module contains the class used for representing a cross section in the map.
"""

import sys

import gi

from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.network.network import Network
from sbaid.view.main_page.cross_section_details_popover import CrossSectionDetailsPopover
from sbaid.view.main_page.cross_section_icon import CrossSectionIcon

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
    __icon: CrossSectionIcon
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

        self.__icon = CrossSectionIcon()

        self.set_child(self.__icon)

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
            self.__icon.attach_popover(self.__popover)

        self.__popover.popup()

    def __on_clicked(self, click: Gtk.GestureClick, n_press: int, x: float, y: float) -> None:
        self.show_details()
