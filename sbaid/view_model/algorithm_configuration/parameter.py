import sys
import gi
try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Parameter(GObject.GObject):
    name: str = GObject.Property(type=str, flags=GObject.ParamFlags.READABLE)  # type: ignore
    value_type: GLib.VariantType = GObject.Property(type=GLib.VariantType,  # type: ignore
                                                    flags=GObject.ParamFlags.READABLE)
    value: GLib.Variant = GObject.Property(type=GObject.TYPE_VARIANT)  # type: ignore
    inconsistent: bool = GObject.Property(type=bool, default=False,
                                          flags=GObject.ParamFlags.READABLE)  # type: ignore
    selected_tags: Gtk.MultiSelection = GObject.Property(type=Gtk.MultiSelection,  # type: ignore
                                                         flags=GObject.ParamFlags.READABLE)
