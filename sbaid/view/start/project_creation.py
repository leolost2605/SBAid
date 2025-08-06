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

        self.__sim_popover = SimulatorEntryPopover(self.__context)

        self.__enter_name_row = Adw.EntryRow(title="Name")

        enter_simulator_button = Gtk.MenuButton(label="Select", popover=self.__sim_popover)
        enter_sim_row = Adw.ActionRow(title="Simulator")
        enter_sim_row.add_suffix(enter_simulator_button)

        self.__project_path_row = Adw.EntryRow(title="Project Path")

        enter_button = Gtk.Button(label="Create", margin_top=12)
        enter_button.add_css_class("suggested-action")
        enter_button.connect("clicked", self.__on_enter)

        preferences_group = Adw.PreferencesGroup(
            margin_end=12, margin_top=12, margin_bottom=12, margin_start=12,
            valign=Gtk.Align.CENTER)
        preferences_group.add(self.__enter_name_row)
        preferences_group.add(enter_sim_row)
        preferences_group.add(self.__project_path_row)
        preferences_group.add(enter_button)

        clamp = Adw.Clamp(child=preferences_group, maximum_size=400)

        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(clamp)

        self.set_child(main_view)
        self.set_title("Project Creation")

    async def __create_project_coro(self) -> None:
        name = self.__enter_name_row.get_text()
        sim_path = self.__sim_popover.path
        sim_type = self.__sim_popover.type
        proj_path = self.__project_path_row.get_text()

        if name and sim_type and proj_path and sim_path:
            proj_id = await self.__context.create_project(name, sim_type, sim_path, proj_path)
            self.activate_action("win.open-project", GLib.Variant.new_string(proj_id))

    def __on_enter(self, widget: Gtk.Widget) -> None:
        sbaid.common.run_coro_in_background(self.__create_project_coro())
