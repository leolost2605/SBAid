"""
This module contains the class that represents the result of simulation.
"""
import datetime

import gi
import sys

from sbaid.model.results.result import Result

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, GLib, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Result(GObject.GObject):
    """
    This class represents the result of simulation.
    """

    id: str = GObject.Property(type=str)
    name: str = GObject.Property(type=str)
    creation_date_time: datetime = GObject.Property(type=datetime)
    project_name: str = GObject.Property(type=str)

    selected_tags: Gtk.MultiSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    selected_tags: GObject.Property(  # type: ignore
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    previews: GObject.Property(  # type: ignore
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    cross_section: Gtk.MultiSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    diagram_types: Gtk.SingleSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    formats: Gtk.SingleSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, result: Result, available_tags: Gio.ListModel):
        id = result.id
        name = result.name
        creation_date_time = result.creation_date_time
        project_name = result.project_name
        selected_tags = result.selected_tags
        previews = result.previews
        cross_section = result.cross_section
        diagram_types = result.diagram_types
        formats = result.formats

        self.result: Result = result
        self.available_tags = available_tags
        super().__init__(available_tags=Gtk.MultiSelection.new(self.manager.available_tags))
