"""
This module contains the algo configs dialog.
"""

import sys
from typing import cast

import gi

from sbaid import common
from sbaid.view.parameter_editing.cross_section_row import CrossSectionRow
from sbaid.view.parameter_editing.param_cell import ParamCell, ParamCellType
from sbaid.view_model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.view_model.algorithm_configuration.algorithm_configuration_manager import \
    AlgorithmConfigurationManager
from sbaid.view_model.algorithm_configuration.parameter import Parameter
from sbaid.view_model.network.cross_section import CrossSection

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class _AlgoConfigView(Adw.Bin):
    __name_entry_row: Adw.EntryRow
    __eval_interval_row: Adw.SpinRow
    __display_interval_row: Adw.SpinRow
    __script_path_row: Adw.ActionRow

    __name_binding: GObject.Binding | None = None
    __eval_interval_binding: GObject.Binding | None = None
    __display_interval_binding: GObject.Binding | None = None
    __script_path_binding: GObject.Binding | None = None

    __search_entry: Gtk.SearchEntry
    __filter: Gtk.CustomFilter
    __parameter_model: Gtk.FilterListModel
    __cross_sections_list_view: Gtk.ListView

    __algo_config: AlgorithmConfiguration | None = None

    def __init__(self) -> None:
        super().__init__()

        self.__name_entry_row = Adw.EntryRow()
        self.__name_entry_row.set_title("Name")

        self.__eval_interval_row = Adw.SpinRow.new_with_range(1, 9999999999, 10)
        self.__eval_interval_row.set_title("Evaluation Interval")

        self.__display_interval_row = Adw.SpinRow.new_with_range(1, 9999999999, 10)
        self.__display_interval_row.set_title("Display Interval")

        script_path_button = Gtk.Button.new_with_label("Select...")
        script_path_button.set_valign(Gtk.Align.CENTER)
        script_path_button.connect("clicked", self.__on_script_path_clicked)

        self.__script_path_row = Adw.ActionRow()
        self.__script_path_row.set_title("Script Path")
        self.__script_path_row.add_suffix(script_path_button)

        preferences_group = Adw.PreferencesGroup()
        preferences_group.add(self.__name_entry_row)
        preferences_group.add(self.__eval_interval_row)
        preferences_group.add(self.__display_interval_row)
        preferences_group.add(self.__script_path_row)

        self.__search_entry = Gtk.SearchEntry()
        self.__search_entry.connect("search-changed", self.__on_search_entry_changed)

        self.__filter = Gtk.CustomFilter.new(self.__filter_func)

        self.__parameter_model = Gtk.FilterListModel.new(None, self.__filter)

        selection_model = Gtk.MultiSelection.new(self.__parameter_model)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self.__setup_param_name_cell)
        name_factory.connect("bind", self.__bind_param_cell)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)
        name_column.set_expand(True)

        value_factory = Gtk.SignalListItemFactory()
        value_factory.connect("setup", self.__setup_param_value_cell)
        value_factory.connect("bind", self.__bind_param_cell)

        value_column = Gtk.ColumnViewColumn.new("Value", value_factory)

        tag_factory = Gtk.SignalListItemFactory()
        tag_factory.connect("setup", self.__setup_param_tags_cell)
        tag_factory.connect("bind", self.__bind_param_cell)

        tag_column = Gtk.ColumnViewColumn.new("Tags", tag_factory)

        column_view = Gtk.ColumnView.new(selection_model)
        column_view.set_hexpand(True)
        column_view.set_vexpand(True)
        column_view.append_column(name_column)
        column_view.append_column(value_column)
        column_view.append_column(tag_column)

        column_view_scrolled = Gtk.ScrolledWindow(child=column_view, propagate_natural_width=True,
                                                  propagate_natural_height=True)

        column_view_frame = Gtk.Frame(child=column_view_scrolled)

        cross_sections_check_button = Gtk.CheckButton.new_with_label("Cross Sections")
        cross_sections_check_button.connect("toggled", self.__on_toggled)

        cross_section_factory = Gtk.SignalListItemFactory()
        cross_section_factory.connect("setup", self.__setup_cross_section_row)
        cross_section_factory.connect("bind", self.__bind_cross_section_row)

        self.__cross_sections_list_view = Gtk.ListView.new(None, cross_section_factory)
        self.__cross_sections_list_view.set_vexpand(True)

        cross_sections_scrolled = Gtk.ScrolledWindow(
            child=self.__cross_sections_list_view, propagate_natural_width=True,
            propagate_natural_height=True)

        cross_sections_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        cross_sections_box.append(cross_sections_check_button)
        cross_sections_box.append(cross_sections_scrolled)

        cross_sections_frame = Gtk.Frame(child=cross_sections_box)

        import_button = Gtk.Button.new_with_label("Import")
        import_button.connect("clicked", self.__on_import_clicked)

        grid = Gtk.Grid(margin_end=12, margin_top=12, margin_bottom=12, margin_start=12)
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.attach(preferences_group, 0, 1, 1, 1)
        grid.attach(self.__search_entry, 1, 0, 1, 1)
        grid.attach(column_view_frame, 1, 1, 1, 1)
        grid.attach(cross_sections_frame, 2, 1, 1, 1)
        grid.attach(import_button, 2, 2, 1, 1)

        self.set_child(grid)

    def __on_search_entry_changed(self, entry: Gtk.SearchEntry) -> None:
        self.__filter.changed(Gtk.FilterChange.DIFFERENT)

    def __filter_func(self, param: Parameter) -> bool:
        if self.__search_entry.get_text().strip() == "":
            return True

        return self.__search_entry.get_text().strip() in param.name


    def __setup_param_name_cell(self, factory: Gtk.SignalListItemFactory,
                                obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        list_item.set_child(ParamCell(ParamCellType.NAME))

    def __setup_param_value_cell(self, factory: Gtk.SignalListItemFactory,
                                 obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        list_item.set_child(ParamCell(ParamCellType.VALUE))

    def __setup_param_tags_cell(self, factory: Gtk.SignalListItemFactory,
                                obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        list_item.set_child(ParamCell(ParamCellType.TAGS))

    def __bind_param_cell(self, factory: Gtk.SignalListItemFactory,
                          obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        item = cast(Parameter, list_item.get_item())
        cell = cast(ParamCell, list_item.get_child())
        cell.bind(item)

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

    def __on_script_path_clicked(self, button: Gtk.Button) -> None:
        common.run_coro_in_background(self.__collect_script_path())

    async def __collect_script_path(self) -> None:
        dialog = Gtk.FileDialog()

        try:
            file = await dialog.open(self.get_root())
        except Exception as e:
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        self.__algo_config.script_path = file.get_path()

    def __on_toggled(self, check_button: Gtk.CheckButton) -> None:
        if check_button.get_active():
            self.__algo_config.parameter_configuration.selected_cross_sections.select_all()
        else:
            self.__algo_config.parameter_configuration.selected_cross_sections.unselect_all()

    def __on_import_clicked(self, button: Gtk.Button) -> None:
        common.run_coro_in_background(self.__collect_import_file())

    async def __collect_import_file(self) -> None:
        dialog = Gtk.FileDialog()

        try:
            file = await dialog.open(self.get_root())
        except Exception as e:
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        await self.__algo_config.parameter_configuration.import_parameter_values(file)

    def set_algo_config(self, config: AlgorithmConfiguration) -> None:
        """
        Sets the algo config that is currently edited
        :param config: the config to edit
        """
        if self.__name_binding:
            self.__name_binding.unbind()

        self.__name_binding = config.bind_property(
            "name", self.__name_entry_row, "text",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        if self.__eval_interval_binding:
            self.__eval_interval_binding.unbind()

        self.__eval_interval_binding = config.bind_property(
            "evaluation-interval", self.__eval_interval_row, "value",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        if self.__display_interval_binding:
            self.__display_interval_binding.unbind()

        self.__display_interval_binding = config.bind_property(
            "display-interval", self.__display_interval_row, "value",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        if self.__script_path_binding:
            self.__script_path_binding.unbind()

        self.__script_path_binding = config.bind_property(
            "script-path", self.__script_path_row, "subtitle",
            GObject.BindingFlags.SYNC_CREATE)

        param_config = config.parameter_configuration
        self.__parameter_model.set_model(param_config.parameters)
        self.__cross_sections_list_view.set_model(param_config.selected_cross_sections)

        self.__algo_config = config


class AlgoConfigsDialog(Adw.Window):
    """
    Represents a dialog shown to the user to allow configuring the algorithm configurations
    of a project.
    """

    __manager: AlgorithmConfigurationManager
    __algo_config_view: _AlgoConfigView
    __split_view: Adw.NavigationSplitView

    def __init__(self, algo_config_manager: AlgorithmConfigurationManager):
        super().__init__()

        self.__manager = algo_config_manager

        collapse_button = Gtk.Button.new_from_icon_name("collapse")
        collapse_button.connect("clicked", self.__on_collapse_clicked)

        content_header_bar = Adw.HeaderBar()
        # content_header_bar.pack_start(collapse_button) TODO

        self.__algo_config_view = _AlgoConfigView()

        content_toolbar_view = Adw.ToolbarView(content=self.__algo_config_view)
        content_toolbar_view.add_top_bar(content_header_bar)

        content_page = Adw.NavigationPage.new(content_toolbar_view, "Algorithm Configuration")

        header_bar = Adw.HeaderBar(show_title=False)

        sidebar = Gtk.ListBox()
        sidebar.set_selection_mode(Gtk.SelectionMode.SINGLE)
        sidebar.bind_model(algo_config_manager.algorithm_configurations,
                           self.__create_algo_config_row)
        sidebar.connect("row-selected", self.__on_row_selected)

        scrolled_sidebar = Gtk.ScrolledWindow(child=sidebar)

        add_button = Gtk.Button.new_with_label("+ Add")
        add_button.set_halign(Gtk.Align.START)
        add_button.set_margin_top(6)
        add_button.set_margin_start(6)
        add_button.set_margin_bottom(6)
        add_button.connect("clicked", self.__on_add_clicked)

        sidebar_view = Adw.ToolbarView()
        sidebar_view.add_top_bar(header_bar)
        sidebar_view.set_content(scrolled_sidebar)
        sidebar_view.add_bottom_bar(add_button)

        sidebar_page = Adw.NavigationPage.new(sidebar_view, "Algorithm Configurations")

        self.__split_view = Adw.NavigationSplitView()
        self.__split_view.set_content(content_page)
        self.__split_view.set_sidebar(sidebar_page)

        self.set_content(self.__split_view)

    def __on_collapse_clicked(self, button: Gtk.Button) -> None:
        self.__split_view.set_collapsed(not self.__split_view.get_collapsed())

    def __create_algo_config_row(self, algo_config: AlgorithmConfiguration) -> Gtk.Widget:
        label = Gtk.Label()
        algo_config.bind_property("name", label, "label", GObject.BindingFlags.SYNC_CREATE)
        return label

    def __on_row_selected(self, list_box: Gtk.ListBox, row: Gtk.ListBoxRow) -> None:
        if not row:
            return

        config = cast(AlgorithmConfiguration,
                      self.__manager.algorithm_configurations.get_item(row.get_index()))
        self.__algo_config_view.set_algo_config(config)

    def __on_add_clicked(self, button: Gtk.Button) -> None:
        common.run_coro_in_background(self.__add_algo_config())

    async def __add_algo_config(self) -> None:
        await self.__manager.create_algorithm_configuration()
