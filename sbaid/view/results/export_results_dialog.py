import sys
from typing import Any, cast

import gi

from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.view.results.cross_section_row import CrossSectionRow
from sbaid.view_model.network.cross_section import CrossSection

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ExportResultsDialog(Adw.Window):
    __result: Any

    def __init__(self, result: Any) -> None:
        super().__init__()

        self.__result = result

        header_bar = Adw.HeaderBar()

        diagram_type_name_expression = Gtk.PropertyExpression.new(DiagramType, None, "name")

        diagram_type_drop_down = Gtk.DropDown.new(result.diagram_types,
                                                  diagram_type_name_expression)

        cross_sections_check_button = Gtk.CheckButton.new_with_label("Cross Sections")
        cross_sections_check_button.set_halign(Gtk.Align.START)
        cross_sections_check_button.connect("toggled", self.__on_toggled)

        cross_section_factory = Gtk.SignalListItemFactory()
        cross_section_factory.connect("setup", self.__setup_cross_section_row)
        cross_section_factory.connect("bind", self.__bind_cross_section_row)

        self.__cross_sections_list_view = Gtk.ListView.new(result.cross_sections,
                                                           cross_section_factory)
        self.__cross_sections_list_view.set_size_request(180, -1)
        self.__cross_sections_list_view.set_vexpand(True)

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

        preview_frame = Gtk.Frame(child=preview_grid_view)

        image_format_name_expression = Gtk.PropertyExpression.new(Adw.EnumListItem, None, "name")

        image_format_drop_down = Gtk.DropDown.new(result.formats, image_format_name_expression)

        export_button = Gtk.Button.new_with_label("Export")
        export_button.add_css_class("suggested-action")
        export_button.set_halign(Gtk.Align.END)

        # TODO: bind selected to the drop downs?

        grid = Gtk.Grid(margin_end=12, margin_top=12, margin_bottom=12, margin_start=12,
                        column_spacing=12, row_spacing=12, column_homogeneous=True)
        grid.attach(diagram_type_drop_down, 0, 0, 2, 1)
        grid.attach(cross_sections_frame, 0, 1, 1, 1)
        grid.attach(preview_frame, 1, 1, 1, 1)
        grid.attach(image_format_drop_down, 0, 2, 2, 1)

        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.set_content(grid)
        toolbar_view.add_bottom_bar(export_button)

        self.set_content(toolbar_view)
        self.set_title("Export " + result.name)

    def __setup_cross_section_row(self, factory: Gtk.SignalListItemFactory,
                                  obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        list_item.set_child(CrossSectionRow())

    def __bind_cross_section_row(self, factory: Gtk.SignalListItemFactory,
                                 obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        item = cast(CrossSection, list_item.get_item())
        cell = cast(CrossSectionRow, list_item.get_child())
        cell.bind(item)

    def __on_toggled(self, check_button: Gtk.CheckButton) -> None:
        if self.__result is None:
            return

        if check_button.get_active():
            self.__result.cross_sections.select_all()
        else:
            self.__result.cross_sections.unselect_all()

    def __setup_preview(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem) -> None:
        image = Gtk.Image()
        item.set_child(image)

    def __bind_preview(self, factory: Gtk.SignalListItemFactory, item: Gtk.ListItem) -> None:
        image = cast(Gtk.Image, item.get_child())
        preview = cast(Image, item.get_child())
        image.set_from_paintable(preview)
