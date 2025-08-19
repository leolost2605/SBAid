"""
This module contains the CrossSectionRow class displaying a cross section.
"""

import sys

import gi

from sbaid.view_model.results.result import CrossSectionSnapshotWrapper

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionRow(Adw.Bin):
    """
    This class displays a cross section while allowing itself to be recycled
    by allowing new cross sections to be set.
    """
    __label: Gtk.Label
    __label_binding: GObject.Binding | None = None

    def __init__(self) -> None:
        super().__init__()

        self.__label = Gtk.Label()
        self.set_child(self.__label)

    def bind(self, cross_section: CrossSectionSnapshotWrapper) -> None:
        """
        Binds the given cross section to this row. Replaces any other cross section that may
        have been previously bound.
        :param cross_section: the cross section to bind
        """

        self.__label.set_label(cross_section.cs_info[1])
