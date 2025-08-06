"""This module contains the simulator entry popover."""
import sys
from typing import cast

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
    @property
    def type(self) -> SimulatorType:
        """Getter for the simulator type entry."""
        return cast(SimulatorType, self.__enter_type_drop_down.get_selected_item())

    @property
    def path(self) -> str:
        """Getter for the simulator file path entry."""
        return self.__enter_path_row.get_text()

    def __init__(self,  context: Context):
        super().__init__()
        self.__context = context

        self.__enter_type_drop_down = Gtk.DropDown()
        self.__enter_type_drop_down.set_model(self.__context.simulator_types)
        self.__enter_type_drop_down.set_expression(Gtk.PropertyExpression.new(SimulatorType, None,
                                                                              "name"))

        self.__enter_path_row = Adw.EntryRow(title="Simulator Path")

        preferences_group = Adw.PreferencesGroup()
        preferences_group.set_title("Simulator Options")

        preferences_group.add(self.__enter_type_drop_down)
        preferences_group.add(self.__enter_path_row)

        self.set_child(preferences_group)
