"""This module contains the project creation page."""
import sys
from typing import Any

import gi

import sbaid.common
from sbaid.view_model.context import Context
from sbaid.view.start.simulator_entry_popover import SimulatorEntryPopover

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ProjectCreation(Adw.NavigationPage):
    """This class represents the project creation page, that is used to create new projects."""
    def __init__(self, context: Context):
        super().__init__()
        self.__context = context

        self.sim_popover = SimulatorEntryPopover(self.__context)

        self.enter_name = Adw.EntryRow(title="Name")

        self.enter_simulator = Gtk.Button(label="Simulator")
        self.enter_simulator.connect("clicked", self.__on_enter_simulator)

        self.enter_project_path = Adw.EntryRow(title="Project Path")

        self.enter_name.set_action_target_value(GLib.Variant.new_string(self.enter_name.get_text()))

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        box.append(self.enter_name)
        box.append(self.enter_simulator)
        box.append(self.enter_project_path)

        self.enter = Gtk.Button(label="Enter")
        self.enter.connect("clicked", self.__on_enter)

        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.add_bottom_bar(self.enter)

        main_view.set_content(box)

        self.set_child(main_view)
        self.set_title("Project Creation")

    def __on_enter_simulator(self, widget: Gtk.Widget) -> None:
        self.sim_popover.set_parent(widget)
        self.sim_popover.popup()

    async def __create_project_coro(self, args: Any) -> None:
        proj_id = await self.__context.create_project(self.enter_name.get_text(),
                                                      self.sim_popover.type,
                                                      self.enter_project_path.get_text(),
                                                      self.sim_popover.path)
        self.activate_action("win.open-project", GLib.Variant.new_string(proj_id))

    def __on_enter(self, widget: Gtk.Widget) -> None:
        name = self.enter_name.get_text()
        proj_path = self.enter_project_path.get_text()
        sim_type = self.sim_popover.type
        sim_path = self.sim_popover.type

        if name and sim_type and proj_path and sim_path:
            sbaid.common.run_coro_in_background(self.__create_project_coro(
                self.enter_name.get_text(),))
