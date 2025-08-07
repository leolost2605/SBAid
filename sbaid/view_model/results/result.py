"""
This module contains the class that represents the result of simulation.
"""
import gi
import sys
from gi.repository import GLib

from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.diagram_exporter import DiagramExporter
from sbaid.model.results.result import Result as ModelResult

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import GObject, Gtk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

class _ImageFormatWrapper(GObject.GObject):
    image_format: ImageFormat
    def __init__(self, image_format: ImageFormat):
        super().__init__()
        self.format = image_format

class _CrossSectionSnapshotWrapper(GObject.GObject):
    """todo"""
    cross_section_id: str
    cross_section_name: str
    def __init__(self, cs_snapshot: CrossSectionSnapshot):
        super().__init__()
        # cross_section_id = cs_snapshot.cross_section_id
        cross_section_name = cs_snapshot.cross_section_name

class Result(GObject.GObject):
    """
    This class represents the result of simulation.
    """
    __diagram_exporter: DiagramExporter
    __result: ModelResult
    __previews: Gio.ListStore

    id: str = GObject.Property(type=str)

    @id.getter  # type: ignore
    def id(self) -> str:
        """Returns the id of the result."""
        return self.__result.id

    name: str = GObject.Property(type=str)

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the result."""
        return self.__result.result_name

    @name.setter  #type: ignore
    def name(self, name: str) -> None:
        """Sets the name of the result."""
        self.__result.result_name = name

    creation_date_time: GLib.DateTime = GObject.Property(type=GLib.DateTime)

    @creation_date_time.getter  # type: ignore

    def creation_date_time(self) -> GLib.DateTime:
        """Returns the creation date of the result."""
        return self.__result.creation_date_time

    project_name: str = GObject.Property(type=str)

    @project_name.getter  # type: ignore
    def project_name(self) -> str:
        """Returns the name of the project."""
        return self.__result.project_name

    previews: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]
    @previews.getter # type: ignore
    def previews(self) -> Gio.ListModel:
        """Returns the previews of the result."""
        return self.__previews

    selected_tags: Gtk.MultiSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    cross_section: Gtk.MultiSelection = GObject.Property(  # type: ignore
        type=Gtk.MultiSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    diagram_types: Gtk.SingleSelection = GObject.Property(  # type: ignore
        type=Gtk.SingleSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    formats: Gtk.SingleSelection = GObject.Property(  # type: ignore
        type=Gtk.SingleSelection,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, result: ModelResult, available_tags: Gio.ListModel):
        self.__result = result

        self.selected_tags = result.selected_tags

        self.__diagram_exporter = DiagramExporter()
        self.__previews = Gio.ListStore.new(SeabornImage)
        super().__init__(selected_tags=Gtk.MultiSelection.new(available_tags),
                         diagram_types=Gtk.SingleSelection.new(self.__diagram_exporter.available_diagram_types),
                         cross_section=Gtk.MultiSelection.new(self.__get_cross_section_selection(result)),
                         formats=Gtk.SingleSelection.new(self.__get_format_selection()))

    def save_diagrams(self, path: str) -> None:
        """Saves diagrams to a file."""
        image_format = ImageFormat(self.formats.get_selected())

        for cross_sections in self.cross_section:
            """todo"""


    def __get_cross_section_selection(self, result: ModelResult) -> Gio.ListModel:
        """Returns the cross section information """
        cross_section__selections = Gio.ListStore.new(_CrossSectionSnapshotWrapper)
        return cross_section__selections

    def __get_format_selection(self) -> Gio.ListModel:

        format_selections = Gio.ListStore.new(ImageFormat)
        for image_format in ImageFormat:
            format_selections.append(_ImageFormatWrapper(image_format))
        return format_selections


    def __load_previews(self):
        """Loads previews from a file."""
