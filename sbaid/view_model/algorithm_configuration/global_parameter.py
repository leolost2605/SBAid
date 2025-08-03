"""
This module contains the parameter implementation that represents a global parameter.
"""

import sys
from typing import cast
import gi

from sbaid.common.tag import Tag
from sbaid.view_model.algorithm_configuration.parameter import Parameter
from sbaid.model.algorithm_configuration.parameter import Parameter as ModelParameter
from sbaid import common

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GLib, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class GlobalParameter(Parameter):
    """
    This class represents a global parameter. It exists only once for an algorithm.
    """
    __parameter: ModelParameter
    __tags: Gtk.MultiSelection

    @Parameter.name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the parameter."""
        return self.__parameter.name

    @Parameter.value_type.getter  # type: ignore
    def value_type(self) -> GLib.VariantType:
        """Returns the value type of the parameter."""
        return self.__parameter.value_type

    @Parameter.value.getter  # type: ignore
    def value(self) -> GLib.Variant:
        """Returns the value of the parameter."""
        return self.__parameter.value

    @Parameter.value.setter  # type: ignore
    def value(self, value: GLib.Variant) -> None:
        """Sets the value of the parameter."""
        if not value.is_of_type(self.value_type):
            raise ValueError("Value must be of the correct type for the parameter. Got "
                             f"{value.get_type_string()}, expected {self.value_type.dup_string()}")

        self.__parameter.value = value

    @Parameter.selected_tags.getter  # type: ignore
    def selected_tags(self) -> Gtk.MultiSelection:
        """Returns the list of selected tags of the parameter."""
        return self.__tags

    def __init__(self, parameter: ModelParameter, available_tags: Gio.ListModel) -> None:
        super().__init__()
        self.__parameter = parameter
        self.__tags = Gtk.MultiSelection.new(available_tags)

        for i, tag in enumerate(common.list_model_iterator(available_tags)):
            for selected_tag in common.list_model_iterator(parameter.selected_tags):
                if selected_tag == tag:
                    self.__tags.select_item(i, False)
                    break

        self.__tags.connect("selection_changed", self.__on_selection_changed)

    def __on_selection_changed(self, pos: int, n_items: int) -> None:
        for i in range(pos, n_items):
            tag = cast(Tag, self.__tags.get_item(i))
            if self.__tags.is_selected(i):
                self.__parameter.add_tag(tag)
            else:
                self.__parameter.remove_tag(tag)
