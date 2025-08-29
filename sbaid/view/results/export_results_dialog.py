"""
This module contains the export results dialog.
"""

import sys
from typing import cast

import gi

from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.view import utils
from sbaid.view.results.cross_section_row import CrossSectionRow
from sbaid.view_model.results.result import Result, CrossSectionSnapshotWrapper

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ExportResultsDialog(Adw.Window):
    """
    This class is used to shown an export results dialog to the user where they can
    choose what data about the results to export.
    """

    __result: Result

    # pylint: disable=too-many-locals, too-many-statements
    def __init__(self, result: Result) -> None:
        super().__init__(default_width=700, default_height=700)

        self.__result = result

        header_bar = Adw.HeaderBar()

        diagram_type_name_expression = Gtk.PropertyExpression.new(DiagramType, None, "name")

        diagram_type_drop_down = Gtk.DropDown.new(result.diagram_types,
                                                  diagram_type_name_expression)
        diagram_type_drop_down.bind_property("selected", result.diagram_types, "selected")

        cross_sections_check_button = Gtk.CheckButton.new_with_label("Cross Sections")
        cross_sections_check_button.set_halign(Gtk.Align.START)
        cross_sections_check_button.connect("toggled", self.__on_toggled)

        cross_section_factory = Gtk.SignalListItemFactory()
        cross_section_factory.connect("setup", self.__setup_cross_section_row)
        cross_section_factory.connect("bind", self.__bind_cross_section_row)

        self.__cross_sections_list_view = Gtk.ListView.new(result.cross_section,
                                                           cross_section_factory)
        self.__cross_sections_list_view.set_size_request(180, -1)
        self.__cross_sections_list_view.set_vexpand(True)
        self.__cross_sections_list_view.set_enable_rubberband(True)

        cross_sections_scrolled = Gtk.ScrolledWindow(
            child=self.__cross_sections_list_view, propagate_natural_width=True,
            propagate_natural_height=True)

        cross_sections_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        cross_sections_box.append(cross_sections_check_button)
        cross_sections_box.append(cross_sections_scrolled)

        cross_sections_frame = Gtk.Frame(child=cross_sections_box)

        preview_factory = Gtk.SignalListItemFactory()
        preview_factory.connect("setup", self.__setup_preview)
        preview_factory.connect("bind", self.__bind_preview)

        selection = Gtk.NoSelection.new(result.previews)

        preview_grid_view = Gtk.GridView.new(selection, preview_factory)

        # preview_scrolled = Gtk.ScrolledWindow(child=preview_grid_view, propagate_natural_width=True,
        #                                       propagate_natural_height=True,
        #                                       hscrollbar_policy=Gtk.PolicyType.NEVER)
        #
        # preview_frame = Gtk.Frame(child=preview_scrolled)

        image_format_name_expression = Gtk.PropertyExpression.new(Adw.EnumListItem, None, "name")

        image_format_drop_down = Gtk.DropDown.new(result.formats, image_format_name_expression)
        image_format_drop_down.bind_property("selected", result.formats, "selected")

        export_button = Gtk.Button.new_with_label("Export")
        export_button.add_css_class("suggested-action")
        export_button.set_halign(Gtk.Align.END)
        export_button.set_margin_bottom(6)
        export_button.set_margin_end(6)
        export_button.set_margin_top(6)
        export_button.set_margin_start(6)
        export_button.connect("clicked", self.__on_exported)

        grid = Gtk.Grid(margin_end=12, margin_top=12, margin_bottom=12, margin_start=12,
                        column_spacing=12, row_spacing=12, column_homogeneous=True)
        grid.attach(diagram_type_drop_down, 0, 0, 2, 1)
        grid.attach(cross_sections_frame, 0, 1, 1, 1)
        grid.attach(preview_grid_view, 1, 1, 1, 1)
        grid.attach(image_format_drop_down, 0, 2, 2, 1)

        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.set_content(grid)
        toolbar_view.add_bottom_bar(export_button)

        self.set_content(toolbar_view)
        self.set_title("Export " + result.name)

        utils.run_coro_with_error_reporting(result.load())

    def __setup_cross_section_row(self, factory: Gtk.SignalListItemFactory,
                                  obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        list_item.set_child(CrossSectionRow())

    def __bind_cross_section_row(self, factory: Gtk.SignalListItemFactory,
                                 obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        item = cast(CrossSectionSnapshotWrapper, list_item.get_item())
        cell = cast(CrossSectionRow, list_item.get_child())
        cell.bind(item)

    def __on_toggled(self, check_button: Gtk.CheckButton) -> None:
        if self.__result is None:
            return

        if check_button.get_active():
            self.__result.cross_section.select_all()
        else:
            self.__result.cross_section.unselect_all()

    def __setup_preview(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem) -> None:
        image = Gtk.Picture(content_fit=Gtk.ContentFit.CONTAIN, can_shrink=True)
        item.set_child(image)

    def __bind_preview(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem) -> None:
        image = cast(Gtk.Picture, item.get_child())
        preview = cast(Image, item.get_item())
        image.set_paintable(preview)

    def __on_exported(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(self.__export_diagrams())

    async def __export_diagrams(self) -> None:
        dialog = Gtk.FileDialog()

        try:
            file = await dialog.select_folder(self)  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        self.__result.save_diagrams(file.get_path())
