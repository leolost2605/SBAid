import sys

import gi

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GObject, GLib, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

class SimulatorEntryPopover(Gtk.Popover):
    def __init__(self):
        super().__init__()

        # preferences_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        preferences_group = Adw.PreferencesGroup()
        preferences_group.set_title("Simulator Options")


        self.enter_type = Adw.ComboRow(title="Type")
        self.enter_type = Gtk.DropDown.new_from_strings(["vissim", "dummy"])
        # lm = Gio.ListStore.new(str)
        # lm.append("vissim")
        # lm.append("dummy")
        # self.enter_type.model = lm
        # self.enter_type.connect("entry-activated", self.__on_enter_type)

        self.enter_path = Adw.EntryRow(title="Simulator Path")
        self.enter_path.connect("entry-activated", self.__on_enter_path)

        preferences_group.add(self.enter_type)
        preferences_group.add(self.enter_path)
        # box.append(self.enter_type)
        # box.append(self.enter_path)

        self.set_child(preferences_group)

    def __on_enter_type(self, widget: Gtk.Widget):
        print("entered type")

    def __on_enter_path(self, widget: Gtk.Widget):
        print("entered path")