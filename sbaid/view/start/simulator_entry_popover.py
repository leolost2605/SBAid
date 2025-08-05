"""This module contains the simulator entry popover."""
import sys
from typing import cast, Any

import gi

from sbaid.common.simulator_type import SimulatorType
from sbaid.view_model.context import Context

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class SimulatorEntryPopover(Gtk.Popover):
    """This class contains the simulator entry popover which is used
    to enter the simulator type and simulation file path."""
    __type: SimulatorType
    __path: str

    @property
    def type(self) -> SimulatorType:
        """Getter for the simulator type entry."""
        return self.__type

    @property
    def path(self) -> str:
        """Getter for the simulator file path entry."""
        return self.__path

    def __init__(self,  context: Context):
        super().__init__()
        self.__context = context

        self.enter_type = Gtk.DropDown()
        self.enter_type.set_model(self.__context.simulator_types)
        self.enter_type.set_expression(Gtk.PropertyExpression.new(SimulatorType, None, "name"))
        self.enter_type.connect("notify::selected", self.__on_enter_type)

        self.enter_path = Adw.EntryRow(title="Simulator Path")
        self.enter_path.connect("entry-activated", self.__on_enter_path)

        preferences_group = Adw.PreferencesGroup()
        preferences_group.set_title("Simulator Options")

        preferences_group.add(self.enter_type)
        preferences_group.add(self.enter_path)

        self.set_child(preferences_group)

        self.enter_type.notify("selected")

    def __on_enter_type(self, widget: Gtk.Widget, params: Any) -> None:
        self.__type = cast(SimulatorType, self.enter_type.get_selected_item())

    def __on_enter_path(self, widget: Gtk.Widget) -> None:
        self.__path = self.enter_path.get_text()
