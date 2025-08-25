"""
This module contains the class used for graphically representing a cross section.
"""

import sys

import gi

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionIcon(Adw.Bin):
    """
    An icon used to represent a cross section. It makes sure the bottom part of the
    icon is centered in the widget.
    """

    def __init__(self) -> None:
        super().__init__()

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

    def attach_popover(self, popover: Gtk.Popover) -> None:
        """
        Sets this as the parent of popover in a way that the popover will point
        to the icon exactly.
        """
        popover.set_parent(self.__image)
