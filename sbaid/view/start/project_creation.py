import sys

import gi

from view.start.simulator_entry_popover import SimulatorEntryPopover
from view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ProjectCreation(Adw.NavigationPage):
    def __init__(self):
        super().__init__()
        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)


        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.enter_name = Adw.EntryRow(title="Name")
        self.enter_name.connect("entry-activated", self.__on_enter_name)

        self.enter_simulator = Gtk.Button(label="Simulator")
        self.enter_simulator.connect("clicked", self.__on_enter_simulator)

        self.project_path = Adw.EntryRow(title="Project Path")
        self.project_path.connect("entry-activated", self.__on_enter_project_path)

        self.enter_name.set_action_target_value(GLib.Variant.new_string(self.enter_name.get_text()))

        box.append(self.enter_name)
        box.append(self.enter_simulator)
        box.append(self.project_path)

        main_view.set_content(box)

        self.enter = Gtk.Button(label="Enter")
        self.enter.connect("clicked", self.__on_enter)
        self.enter.set_action_name("win.create-project")

        main_view.add_bottom_bar(self.enter)

        self.set_child(main_view)
        self.set_title("Project Creation")

    def __on_enter_name(self, widget: Gtk.Widget) -> None:
        self.__name = self.enter_name.get_text()
        print("entered name: ", self.__name)

    def __on_enter_simulator(self, widget: Gtk.Widget) -> None:
        self.sim_popover = SimulatorEntryPopover()
        self.sim_popover.set_parent(widget)
        self.sim_popover.popup()

    def __on_enter_project_path(self, widget: Gtk.Widget) -> None:
        self.__project_path = self.project_path.get_text()
        print("entered project: ", self.__project_path)

    def __on_enter(self, widget: Gtk.Widget, sim_type_id: str, sim_type_name: str,
                   sim_path: str) -> None:
        print("entered")
        self.__name
        self.__project_path
        self.sim_popover.get

        self.enter.activate_action("create-project")
        # name_variant = GLib.Variant.new_string(proj_name)
        # sequence = GLib.Sequence()
        # sequence.append(None)
        # elements = GLib.Variant.new_array(GLib.VariantType('s'), None)
        # self.enter.activate_action("create-project", GLib.Variant.new_fixed_array(

