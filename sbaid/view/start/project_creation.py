"""This module contains the project creation page."""
import sys
from typing import cast

import gi

from sbaid.common.simulator_type import SimulatorType
from sbaid.view import utils
from sbaid.view_model.context import Context

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

        self.__enter_name_row = Adw.EntryRow(title="Name")

        self.__simulator_row = Adw.ComboRow(title="Simulator")
        self.__simulator_row.set_expression(Gtk.PropertyExpression.new(
            SimulatorType, None, "name"))
        self.__simulator_row.set_model(context.simulator_types)

        select_simulation_path_button = Gtk.Button.new_with_label("Select...")
        select_simulation_path_button.set_valign(Gtk.Align.CENTER)
        select_simulation_path_button.connect("clicked", self.__on_simulation_path_clicked)

        self.__simulation_path_row = Adw.ActionRow(title="Simulation File")
        self.__simulation_path_row.add_suffix(select_simulation_path_button)

        select_project_path_button = Gtk.Button.new_with_label("Select...")
        select_project_path_button.set_valign(Gtk.Align.CENTER)
        select_project_path_button.connect("clicked", self.__on_project_path_clicked)

        self.__project_path_row = Adw.ActionRow(title="Project Folder")
        self.__project_path_row.add_suffix(select_project_path_button)

        enter_button = Gtk.Button(label="Create", margin_top=12)
        enter_button.add_css_class("suggested-action")
        enter_button.connect("clicked", self.__on_enter)

        preferences_group = Adw.PreferencesGroup(
            margin_end=12, margin_top=12, margin_bottom=12, margin_start=12,
            valign=Gtk.Align.CENTER)
        preferences_group.add(self.__enter_name_row)
        preferences_group.add(self.__simulator_row)
        preferences_group.add(self.__simulation_path_row)
        preferences_group.add(self.__project_path_row)
        preferences_group.add(enter_button)

        clamp = Adw.Clamp(child=preferences_group, maximum_size=400)

        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(clamp)

        self.set_child(main_view)
        self.set_title("Project Creation")

    def __on_simulation_path_clicked(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(self.__collect_simulation_path())

    async def __collect_simulation_path(self) -> None:
        dialog = Gtk.FileDialog()

        try:
            file = await dialog.open(self.get_root())  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        self.__simulation_path_row.set_subtitle(file.get_path())

    def __on_project_path_clicked(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(self.__collect_project_folder())

    async def __collect_project_folder(self) -> None:
        dialog = Gtk.FileDialog()

        try:
            file = await dialog.select_folder(self.get_root())  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        self.__project_path_row.set_subtitle(file.get_path())

    async def __create_project_coro(self) -> None:
        name = self.__enter_name_row.get_text()
        sim_type = cast(SimulatorType, self.__simulator_row.get_selected_item())
        sim_path = self.__simulation_path_row.get_subtitle()
        proj_path = self.__project_path_row.get_subtitle()

        if name and sim_type and proj_path and sim_path:
            proj_id = await self.__context.create_project(name, sim_type, sim_path, proj_path)
            self.activate_action("win.open-project", GLib.Variant.new_string(proj_id))

    def __on_enter(self, widget: Gtk.Widget) -> None:
        utils.run_coro_with_error_reporting(self.__create_project_coro())
