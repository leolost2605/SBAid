"""
This module contains the class that represents the result of simulation.
"""
import os
from typing import Tuple
import sys
import gi

from sbaid import common
from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_snapshot import CrossSectionSnapshot
from sbaid.model.results.diagram_exporter import DiagramExporter
from sbaid.model.results.result import Result as ModelResult
from sbaid.model.results.snapshot import Snapshot

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import GObject, Gtk, Gio, GLib, Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionSnapshotWrapper(GObject.GObject):
    """Wrapper class containing cross-section snapshot information."""

    cs_info: Tuple[str, str]

    def __init__(self, cs_snapshot: CrossSectionSnapshot):
        super().__init__()
        self.cs_info = cs_snapshot.cross_section_id, cs_snapshot.cross_section_name


class Result(GObject.GObject):
    """
    This class represents the result of simulation.
    """
    id = GObject.Property(type=str)

    @id.getter  # type: ignore
    def id(self) -> str:
        """Returns the id of the result."""
        return self.__result.id

    name: str = GObject.Property(type=str)  # type: ignore

    @name.getter  # type: ignore
    def name(self) -> str:
        """Returns the name of the result."""
        return self.__result.result_name

    @name.setter  # type: ignore
    def name(self, name: str) -> None:
        """Sets the name of the result."""
        self.__result.result_name = name

    creation_date_time: GLib.DateTime = GObject.Property(type=GLib.DateTime)  # type: ignore

    @creation_date_time.getter  # type: ignore
    def creation_date_time(self) -> GLib.DateTime:
        """Returns the creation date of the result."""
        return self.__result.creation_date_time

    project_name: str = GObject.Property(type=str)  # type: ignore

    @project_name.getter  # type: ignore
    def project_name(self) -> str:
        """Returns the name of the project."""
        return self.__result.project_name

    previews: Gio.ListModel = GObject.Property(type=Gio.ListModel)  # type: ignore[assignment]

    @previews.getter  # type: ignore
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

    __diagram_exporter: DiagramExporter
    __available_diagram_types: Gio.ListModel
    __result: ModelResult
    __previews: Gio.ListStore

    def __init__(self, result: ModelResult, available_tags: Gio.ListModel):
        self.__result = result
        self.__diagram_exporter = DiagramExporter()
        self.__available_diagram_types = self.__diagram_exporter.available_diagram_types
        self.__previews = Gio.ListStore.new(Image)

        super().__init__(selected_tags=Gtk.MultiSelection.new(available_tags),
                         diagram_types=Gtk.SingleSelection.new(self.__available_diagram_types),
                         cross_section=Gtk.MultiSelection.
                         new(self.__get_cross_section_selection(result)),
                         formats=Gtk.SingleSelection.new(Adw.EnumListModel.new(ImageFormat)))

        self.formats.connect("selection-changed", self._on_selection_changed)
        self.diagram_types.connect("selection-changed", self._on_selection_changed)
        self.cross_section.connect("selection-changed", self._on_selection_changed)

    def save_diagrams(self, path: str) -> None:
        """Saves diagrams to a file."""
        for image in common.list_model_iterator(self.__previews):
            assert isinstance(image, Image)

            selected_diagram = self.__available_diagram_types.get_item(
                self.diagram_types.get_selected())
            assert isinstance(selected_diagram, DiagramType)

            filename = selected_diagram.name + "_" + self.__get_name_for_file()

            full_path = os.path.join(path, filename)
            image.save_to_file(full_path)

    def __get_name_for_file(self) -> str:
        name_list = []

        for i in range(self.cross_section.get_n_items()):
            if self.cross_section.is_selected(i):
                wrapper = self.cross_section.get_item(i)
                assert isinstance(wrapper, CrossSectionSnapshotWrapper)
                name_list.append(wrapper.cs_info[1])

        return str(name_list)

    def __get_selected_diagram_information(self) -> Tuple[list[str], ImageFormat, DiagramType]:
        image_format = ImageFormat(self.formats.get_selected())
        diagram_type = self.__available_diagram_types.get_item(self.diagram_types.get_selected())
        assert isinstance(diagram_type, DiagramType)

        id_list = []

        for i in range(self.cross_section.get_n_items()):
            if self.cross_section.is_selected(i):
                wrapper = self.cross_section.get_item(i)
                assert isinstance(wrapper, CrossSectionSnapshotWrapper)
                id_list.append(wrapper.cs_info[0])

        return id_list, image_format, diagram_type

    def __get_cross_section_selection(self, result: ModelResult) -> Gio.ListModel:
        """Returns the cross-section information for """
        cross_section_selections = Gio.ListStore.new(CrossSectionSnapshotWrapper)
        snapshot = result.snapshots.get_item(0)
        assert isinstance(snapshot, Snapshot)
        for cross_section in snapshot.cross_section_snapshots:
            assert isinstance(cross_section, CrossSectionSnapshot)
            cross_section_selections.append(CrossSectionSnapshotWrapper(cross_section))
        return cross_section_selections

    def _on_selection_changed(self, selection_mode: Gtk.SelectionModel,
                              position: int, n_items: int) -> None:
        self.__previews.remove_all()
        self.load_previews()

    def load_previews(self) -> None:
        """Loads previews from a file."""
        id_list, image_format, diagram_type = self.__get_selected_diagram_information()

        images = self.__diagram_exporter.get_diagram(
            self.__result, id_list, image_format, diagram_type)

        for image in images:
            self.__previews.append(image)
