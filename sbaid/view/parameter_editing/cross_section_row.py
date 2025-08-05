import sys

import gi

from sbaid.view_model.network.cross_section import CrossSection

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionRow(Adw.Bin):
    __label: Gtk.Label
    __label_binding: GObject.Binding | None = None

    def __init__(self) -> None:
        super().__init__()

        self.__label = Gtk.Label()
        self.set_child(self.__label)

    def bind(self, cross_section: CrossSection) -> None:
        if self.__label_binding:
            self.__label_binding.unbind()

        self.__label_binding = cross_section.bind_property("name", self.__label, "label",
                                                           GObject.BindingFlags.SYNC_CREATE)
