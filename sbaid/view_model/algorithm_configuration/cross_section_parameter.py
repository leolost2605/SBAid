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


class CrossSectionParameter(Parameter):
    __parameters: Gio.ListModel
    __selected_cross_sections: Gtk.MultiSelection
    __tags: Gtk.MultiSelection

    @Parameter.name.getter  # type: ignore
    def name(self) -> str:
        return cast(ModelParameter, self.__parameters.get_item(0)).name

    @Parameter.value_type.getter  # type: ignore
    def value_type(self) -> GLib.VariantType:
        return cast(ModelParameter, self.__parameters.get_item(0)).value_type

    @Parameter.value.getter  # type: ignore
    def value(self) -> GLib.Variant | None:
        if self.inconsistent:
            return None

        for param in common.list_model_iterator(self.__parameters):
            if self.__is_cross_section_selected(param.cross_section.id):
                return cast(ModelParameter, param).value

        return None

    @Parameter.value.setter  # type: ignore
    def value(self, value: GLib.Variant) -> None:
        if not value.is_of_type(self.value_type):
            raise ValueError("Value must be of the correct type for the parameter. Got "
                             f"{value.get_type_string()}, expected {self.value_type.dup_string()}")

        for param in common.list_model_iterator(self.__parameters):
            if self.__is_cross_section_selected(param.cross_section.id):
                param.value = value

    @Parameter.inconsistent.getter
    def inconsistent(self) -> bool:
        common_value = None
        for param in common.list_model_iterator(self.__parameters):
            if self.__is_cross_section_selected(param.cross_section.id):
                if not common_value:
                    common_value = param.value
                elif common_value != param.value:
                    return True

        return False

    @Parameter.selected_tags.getter
    def selected_tags(self) -> Gtk.MultiSelection:
        return self.__tags

    def __init__(self, parameters: Gio.ListModel, selected_cross_sections: Gtk.MultiSelection,
                 available_tags: Gio.ListModel) -> None:
        super().__init__()
        self.__parameters = parameters
        self.__selected_cross_sections = selected_cross_sections
        self.__tags = Gtk.MultiSelection.new(available_tags)

        # TODO: Qualitätssicherung: Tags synchronisieren wenn sie das nicht sind
        #  (sollte nie passieren)
        reference_param = cast(ModelParameter, self.__parameters.get_item(0))
        for i, tag in enumerate(common.list_model_iterator(self.__tags)):
            for selected_tag in common.list_model_iterator(reference_param.selected_tags):
                if selected_tag == tag:
                    self.__tags.select_item(i, False)
                    break

        self.__tags.connect("selection_changed", self.__on_selection_changed)

    def __on_selection_changed(self, pos: int, n_items: int) -> None:
        for i in range(pos, n_items):
            tag = cast(Tag, self.__tags.get_item(i))
            if self.__tags.is_selected(i):
                self.__add_tag(tag)
            else:
                self.__remove_tag(tag)

    def __add_tag(self, tag: Tag) -> None:
        for param in common.list_model_iterator(self.__parameters):
            param.add_tag(tag)

    def __remove_tag(self, tag: Tag) -> None:
        for param in common.list_model_iterator(self.__parameters):
            param.remove_tag(tag)

    def __is_cross_section_selected(self, cs_id: str) -> bool:
        iterator = common.list_model_iterator(self.__selected_cross_sections)
        for i, cross_section in enumerate(iterator):
            if cross_section.id == cs_id:
                return self.__selected_cross_sections.is_selected(i)

        return False
