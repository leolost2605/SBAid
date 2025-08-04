"""
This class contains the interface definition of a parameter.
"""

import sys
import gi
try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Parameter(GObject.GObject):
    """
    This interface represents a algorithm parameter. It can either be global
    or per cross section.
    """
    name: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore
    value_type: GLib.VariantType = GObject.Property(type=GLib.VariantType,  # type: ignore
                                                    flags=GObject.ParamFlags.READABLE)
    value: GLib.Variant = GObject.Property(type=GObject.TYPE_VARIANT)  # type: ignore
    inconsistent: bool = GObject.Property(type=bool, default=False,
                                          flags=GObject.ParamFlags.READABLE)  # type: ignore
    selected_tags: Gtk.MultiSelection = GObject.Property(type=Gtk.MultiSelection,  # type: ignore
                                                         flags=GObject.ParamFlags.READABLE)

    @name.getter  # type: ignore
    def get_name(self) -> str:
        """Returns the name of the parameter."""
        return self.get_name()  # type: ignore

    @value_type.getter  # type: ignore
    def get_value_type(self) -> GLib.VariantType:
        """Returns the value type of the parameter."""
        return self.get_value_type()  # type: ignore

    @value.getter  # type: ignore
    def get_value(self) -> GLib.Variant:
        """Returns the value of the parameter."""
        return self.get_value()  # type: ignore

    @value.setter  # type: ignore
    def set_value(self, value: GLib.Variant) -> None:
        """Sets the value of the parameter."""
        self.set_value(value)

    @inconsistent.getter  # type: ignore
    def get_inconsistent(self) -> bool:
        """Returns whether the selected cross sections have different values."""
        return self.get_inconsistent()  # type: ignore

    @selected_tags.getter  # type: ignore
    def get_selected_tags(self) -> Gtk.MultiSelection:
        """Returns the list of selected tags of the parameter."""
        return self.get_selected_tags()  # type: ignore
