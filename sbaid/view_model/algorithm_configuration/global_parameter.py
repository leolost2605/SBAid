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
    __parameter: ModelParameter
    __tags: Gtk.MultiSelection

    @Parameter.name.getter  # type: ignore
    def name(self) -> str:
        return self.__parameter.name

    @Parameter.value_type.getter  # type: ignore
    def value_type(self) -> GLib.VariantType:
        return self.__parameter.value_type

    @Parameter.value.getter  # type: ignore
    def value(self) -> GLib.Variant:
        return self.__parameter.value

    @Parameter.value.setter  # type: ignore
    def value(self, value: GLib.Variant) -> None:
        if not value.is_of_type(self.value_type):
            raise ValueError("Value must be of the correct type for the parameter. Got "
                             f"{value.get_type_string()}, expected {self.value_type.dup_string()}")

        self.__parameter.value = value

    @Parameter.selected_tags.getter
    def selected_tags(self) -> Gtk.MultiSelection:
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
