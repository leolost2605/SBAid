"""This module contains the results page."""
import sys
from typing import cast, Any

import gi

from sbaid.view import utils
from sbaid.view.common.rename_dialog import RenameDialog
from sbaid.view.results.result_cell import ResultCell, ResultCellType
from sbaid.view_model.results.result import Result
from sbaid.view_model.results.result_manager import ResultManager

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ResultsPage(Adw.NavigationPage):
    """
    This class contains the results page, showing the results from all
    simulations ran on SBAid.
    """

    __manager: ResultManager
    __search_entry: Gtk.SearchEntry
    __filter: Gtk.CustomFilter

    # pylint: disable=too-many-statements
    def __init__(self, result_manager: ResultManager) -> None:  # pylint: disable=too-many-locals
        super().__init__()

        self.__manager = result_manager

        self.__search_entry = Gtk.SearchEntry(placeholder_text="Search Results")
        self.__search_entry.connect("search-changed", self.__on_search_entry_changed)

        header_bar = Adw.HeaderBar()
        header_bar.pack_end(self.__search_entry)

        self.__filter = Gtk.CustomFilter.new(self.__filter_func)

        filter_model = Gtk.FilterListModel.new(result_manager.results, self.__filter)

        column_view = Gtk.ColumnView()
        sorter = column_view.get_sorter()
        sort_model = Gtk.SortListModel.new(filter_model, sorter)
        selection_model = Gtk.NoSelection.new(sort_model)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self.__setup_result_name_cell)
        name_factory.connect("bind", self.__bind_cell)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)
        name_column.set_expand(True)
        name_expr = Gtk.PropertyExpression.new(Result, None, "name")
        name_sorter = Gtk.StringSorter.new(name_expr)
        name_column.set_sorter(name_sorter)

        project_name_factory = Gtk.SignalListItemFactory()
        project_name_factory.connect("setup", self.__setup_project_name_cell)
        project_name_factory.connect("bind", self.__bind_cell)

        project_name_column = Gtk.ColumnViewColumn.new("Project Name", project_name_factory)
        project_name_expr = Gtk.PropertyExpression.new(Result, None, "project_name")
        project_name_sorter = Gtk.StringSorter.new(project_name_expr)
        project_name_column.set_sorter(project_name_sorter)

        date_factory = Gtk.SignalListItemFactory()
        date_factory.connect("setup", self.__setup_date_cell)
        date_factory.connect("bind", self.__bind_cell)

        date_column = Gtk.ColumnViewColumn.new("Date", date_factory)
        date_sorter = Gtk.CustomSorter.new(self.__date_sort_func)
        date_column.set_sorter(date_sorter)

        column_view.set_model(selection_model)
        column_view.set_single_click_activate(True)
        column_view.set_hexpand(True)
        column_view.set_vexpand(True)
        column_view.append_column(name_column)
        column_view.append_column(project_name_column)
        column_view.append_column(date_column)
        column_view.connect("activate", self.__on_activate)

        column_view_scrolled = Gtk.ScrolledWindow(child=column_view, propagate_natural_width=True,
                                                  propagate_natural_height=True)

        column_view_frame = Gtk.Frame(child=column_view_scrolled, margin_top=12, margin_bottom=12,
                                      margin_end=12, margin_start=12)

        toolbar_view = Adw.ToolbarView(content=column_view_frame)
        toolbar_view.add_top_bar(header_bar)

        self.set_child(toolbar_view)
        self.set_title("Results")

        self.install_action("result.rename", "s", self.__on_rename_result)
        self.install_action("result.delete", "s", self.__on_delete_result)

    def __date_sort_func(self, result1: Result, result2: Result, data: Any) -> int:
        return result2.creation_date_time.compare(result1.creation_date_time)

    def __on_search_entry_changed(self, entry: Gtk.SearchEntry) -> None:
        self.__filter.changed(Gtk.FilterChange.DIFFERENT)

    def __filter_func(self, result: Result) -> bool:
        if self.__search_entry.get_text().strip() == "":
            return True

        tokens, ascii_tokens = GLib.str_tokenize_and_fold(self.__search_entry.get_text())

        formatted_time = result.creation_date_time.format("%x %X")

        for token in tokens + ascii_tokens:
            if token in result.name or formatted_time and token in formatted_time:
                return True

        return False

    def __on_activate(self, column_view: Gtk.ColumnView, pos: int) -> None:
        model = column_view.get_model()

        if not model:
            return

        result = cast(Result, model.get_item(pos))  # type: ignore
        self.activate_action("win.export-result", GLib.Variant.new_string(result.id))

    @staticmethod
    def __setup_result_name_cell(factory: Gtk.SignalListItemFactory,
                                 list_item: Gtk.ListItem) -> None:
        list_item.set_child(ResultCell(ResultCellType.RESULT_NAME))

    @staticmethod
    def __setup_project_name_cell(factory: Gtk.SignalListItemFactory,
                                  list_item: Gtk.ListItem) -> None:
        list_item.set_child(ResultCell(ResultCellType.PROJECT_NAME))

    @staticmethod
    def __setup_date_cell(factory: Gtk.SignalListItemFactory,
                          list_item: Gtk.ListItem) -> None:
        list_item.set_child(ResultCell(ResultCellType.DATE))

    @staticmethod
    def __bind_cell(factory: Gtk.SignalListItemFactory,
                    list_item: Gtk.ListItem) -> None:
        item = cast(Result, list_item.get_item())
        cell = cast(ResultCell, list_item.get_child())
        cell.bind(item)

    def __get_result_from_param(self, parameter: GLib.Variant | None) -> Result | None:
        if not parameter:
            return None

        result_id = parameter.get_string()

        if not result_id:
            return None

        for r in self.__manager.results:
            result = cast(Result, r)
            if result.id == result_id:
                return result

        return None

    def __on_delete_result(self, widget: Gtk.Widget, action_name: str,
                           parameter: GLib.Variant | None) -> None:
        result = self.__get_result_from_param(parameter)
        if result:
            utils.run_coro_with_error_reporting(self.__manager.delete_result(result.id))

    def __on_rename_result(self, widget: Gtk.Widget, action_name: str,
                           parameter: GLib.Variant | None) -> None:
        result = self.__get_result_from_param(parameter)

        if result:
            RenameDialog(result.name, result, self.__result_rename_func).present(
                cast(Adw.Window, self.get_root()))

    @staticmethod
    def __result_rename_func(result: Result, new_name: str) -> None:
        result.name = new_name
