"""
This module contains the algo configs dialog.
"""

import sys
from typing import cast, Any

import gi

from sbaid.view import utils
from sbaid.view.parameter_editing.algo_config_row import AlgoConfigRow
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
    from gi.repository import Adw, GLib, Gtk, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class _AlgoConfigView(Adw.Bin):  # pylint: disable=too-many-instance-attributes
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

    algo_config: AlgorithmConfiguration = GObject.Property(  # type: ignore
        type=AlgorithmConfiguration)

    @algo_config.getter  # type: ignore
    def algo_config(self) -> AlgorithmConfiguration:
        """
        Returns the algorithm configuration currently displayed in the view.
        :return: the algo configuration currently displayed in the view
        """
        return self.__algo_config

    @algo_config.setter  # type: ignore
    def algo_config(self, config: AlgorithmConfiguration) -> None:
        """
        Sets the algo config currently displayed in the view
        :param config: the new config to display
        """
        self.__algo_config = config

        if self.__name_binding:
            self.__name_binding.unbind()

        if self.__eval_interval_binding:
            self.__eval_interval_binding.unbind()

        if self.__display_interval_binding:
            self.__display_interval_binding.unbind()

        if self.__script_path_binding:
            self.__script_path_binding.unbind()

        if not config:
            self.__parameter_model.set_model(None)
            self.__cross_sections_list_view.set_model(None)
            return

        self.__name_binding = config.bind_property(
            "name", self.__name_entry_row, "text",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        self.__eval_interval_binding = config.bind_property(
            "evaluation-interval", self.__eval_interval_row, "value",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        self.__display_interval_binding = config.bind_property(
            "display-interval", self.__display_interval_row, "value",
            GObject.BindingFlags.SYNC_CREATE | GObject.BindingFlags.BIDIRECTIONAL)

        self.__script_path_binding = config.bind_property(
            "script-path", self.__script_path_row, "subtitle",
            GObject.BindingFlags.SYNC_CREATE)

        param_config = config.parameter_configuration
        self.__parameter_model.set_model(param_config.parameters)
        self.__cross_sections_list_view.set_model(param_config.selected_cross_sections)

        utils.run_coro_with_error_reporting(param_config.load())

    def __init__(self) -> None:  # pylint: disable=too-many-locals, too-many-statements
        super().__init__()

        self.__name_entry_row = Adw.EntryRow()
        self.__name_entry_row.set_title("Name")

        self.__eval_interval_row = Adw.SpinRow.new_with_range(1, 9999999999, 10)
        self.__eval_interval_row.set_title("Evaluation Interval")
        self.__eval_interval_row.set_subtitle("In seconds")

        self.__display_interval_row = Adw.SpinRow.new_with_range(1, 9999999999, 10)
        self.__display_interval_row.set_title("Display Interval")
        self.__display_interval_row.set_subtitle("In seconds")

        script_path_button = Gtk.Button.new_with_label("Select...")
        script_path_button.set_valign(Gtk.Align.CENTER)
        script_path_button.connect("clicked", self.__on_script_path_clicked)

        self.__script_path_row = Adw.ActionRow()
        self.__script_path_row.set_title("Script Path")
        self.__script_path_row.add_suffix(script_path_button)

        preferences_group = Adw.PreferencesGroup(width_request=300)
        preferences_group.add(self.__name_entry_row)
        preferences_group.add(self.__eval_interval_row)
        preferences_group.add(self.__display_interval_row)
        preferences_group.add(self.__script_path_row)

        parameter_header_label = Gtk.Label.new("Parameters")
        parameter_header_label.set_hexpand(True)
        parameter_header_label.set_xalign(0)
        parameter_header_label.add_css_class("heading")

        parameter_description_label = Gtk.Label.new("Configure the parameters of the algorithm.")
        parameter_description_label.set_wrap(True)
        parameter_description_label.set_xalign(0)
        parameter_description_label.add_css_class("dimmed")

        header_label_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        header_label_box.append(parameter_header_label)
        header_label_box.append(parameter_description_label)

        import_button = Gtk.Button.new_with_label("Import values...")
        import_button.set_halign(Gtk.Align.END)
        import_button.set_valign(Gtk.Align.CENTER)
        import_button.connect("clicked", self.__on_import_clicked)

        header_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
        header_box.append(header_label_box)
        header_box.append(import_button)

        explanation_label = Gtk.Label()
        explanation_label.set_markup(
            "Selecting no cross section will allow to change the global parameters, selecting "
            "at least one cross section will allow to change the parameter values for the selected "
            "cross sections. Refer to the "
            "<a href=\"https://api.pygobject.gnome.org/GLib-2.0/structure-VariantType.html\">"
            "documentation</a> for a detailed explanation of the value types"
        )
        explanation_label.set_wrap(True)

        clamp = Adw.Clamp(child=explanation_label, maximum_size=300)

        explanation_popover = Gtk.Popover(child=clamp)

        info_button = Gtk.MenuButton(icon_name="dialog-information-symbolic",
                                     popover=explanation_popover, halign=Gtk.Align.START)

        self.__search_entry = Gtk.SearchEntry()
        self.__search_entry.connect("search-changed", self.__on_search_entry_changed)

        self.__filter = Gtk.CustomFilter.new(self.__filter_func)

        self.__parameter_model = Gtk.FilterListModel.new(None, self.__filter)

        column_view = Gtk.ColumnView()
        sorter = column_view.get_sorter()
        sort_model = Gtk.SortListModel.new(self.__parameter_model, sorter)
        selection_model = Gtk.MultiSelection.new(sort_model)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self.__setup_param_name_cell)
        name_factory.connect("bind", self.__bind_param_cell)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)
        name_column.set_expand(True)
        expr = Gtk.PropertyExpression.new(Parameter, None, "name")
        name_sorter = Gtk.StringSorter.new(expr)
        name_column.set_sorter(name_sorter)

        value_type_factory = Gtk.SignalListItemFactory()
        value_type_factory.connect("setup", self.__setup_param_value_type_cell)
        value_type_factory.connect("bind", self.__bind_param_cell)

        value_type_column = Gtk.ColumnViewColumn.new("Value Type", value_type_factory)
        value_type_sorter = Gtk.CustomSorter.new(self.__value_type_sort_func)
        value_type_column.set_sorter(value_type_sorter)

        value_factory = Gtk.SignalListItemFactory()
        value_factory.connect("setup", self.__setup_param_value_cell)
        value_factory.connect("bind", self.__bind_param_cell)

        value_column = Gtk.ColumnViewColumn.new("Value", value_factory)

        tag_factory = Gtk.SignalListItemFactory()
        tag_factory.connect("setup", self.__setup_param_tags_cell)
        tag_factory.connect("bind", self.__bind_param_cell)

        tag_column = Gtk.ColumnViewColumn.new("Tags", tag_factory)

        column_view.set_model(selection_model)
        column_view.set_hexpand(True)
        column_view.set_vexpand(True)
        column_view.append_column(name_column)
        column_view.append_column(value_type_column)
        column_view.append_column(value_column)
        column_view.append_column(tag_column)

        column_view_scrolled = Gtk.ScrolledWindow(child=column_view, propagate_natural_width=True,
                                                  propagate_natural_height=True)

        column_view_frame = Gtk.Frame(child=column_view_scrolled)

        cross_sections_check_button = Gtk.CheckButton.new_with_label("Cross Sections")
        cross_sections_check_button.set_halign(Gtk.Align.START)
        cross_sections_check_button.connect("toggled", self.__on_toggled)

        cross_section_factory = Gtk.SignalListItemFactory()
        cross_section_factory.connect("setup", self.__setup_cross_section_row)
        cross_section_factory.connect("bind", self.__bind_cross_section_row)

        self.__cross_sections_list_view = Gtk.ListView.new(None, cross_section_factory)
        self.__cross_sections_list_view.set_size_request(180, -1)
        self.__cross_sections_list_view.set_vexpand(True)

        cross_sections_scrolled = Gtk.ScrolledWindow(
            child=self.__cross_sections_list_view, propagate_natural_width=True,
            propagate_natural_height=True)

        cross_sections_box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        cross_sections_box.append(cross_sections_check_button)
        cross_sections_box.append(cross_sections_scrolled)

        cross_sections_frame = Gtk.Frame(child=cross_sections_box)

        grid = Gtk.Grid(margin_end=12, margin_top=12, margin_bottom=12, margin_start=12)
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.attach(preferences_group, 0, 0, 2, 1)
        grid.attach(header_box, 0, 1, 2, 1)
        grid.attach(info_button, 0, 2, 1, 1)
        grid.attach(self.__search_entry, 1, 2, 1, 1)
        grid.attach(cross_sections_frame, 0, 3, 1, 1)
        grid.attach(column_view_frame, 1, 3, 1, 1)

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

    def __setup_param_value_type_cell(self, factory: Gtk.SignalListItemFactory,
                                      obj: GObject.Object) -> None:
        list_item = cast(Gtk.ListItem, obj)
        list_item.set_child(ParamCell(ParamCellType.VALUE_TYPE))

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
        utils.run_coro_with_error_reporting(self.__collect_script_path())

    async def __collect_script_path(self) -> None:
        if self.__algo_config is None:
            return

        dialog = Gtk.FileDialog()

        try:
            file = await dialog.open(self.get_root())  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        self.__algo_config.script_path = file.get_path()

    def __on_toggled(self, check_button: Gtk.CheckButton) -> None:
        if self.__algo_config is None:
            return

        if check_button.get_active():
            self.__algo_config.parameter_configuration.selected_cross_sections.select_all()
        else:
            self.__algo_config.parameter_configuration.selected_cross_sections.unselect_all()

    def __on_import_clicked(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(self.__collect_import_file())

    async def __collect_import_file(self) -> None:
        if self.__algo_config is None:
            return

        dialog = Gtk.FileDialog()

        try:
            file = await dialog.open(self.get_root())  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Failed to allow the user to choose a file: ", e)
            return

        if file is None:
            return

        await self.__algo_config.parameter_configuration.import_parameter_values(file)

    def __value_type_sort_func(self, parameter1: Parameter, parameter2: Parameter, data: Any)\
            -> int:
        if parameter1.value_type.dup_string() > parameter2.value_type.dup_string():
            return 1
        if parameter1.value_type.dup_string() < parameter2.value_type.dup_string():
            return -1
        return 0


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

        self.install_action("algo-config.delete", "s", self.__on_delete)

        self.__manager = algo_config_manager

        content_header_bar = Adw.HeaderBar()

        self.__algo_config_view = _AlgoConfigView()
        algo_config_manager.algorithm_configurations.bind_property(
            "selected-item", self.__algo_config_view, "algo-config",
            GObject.BindingFlags.SYNC_CREATE)

        content_toolbar_view = Adw.ToolbarView(content=self.__algo_config_view)
        content_toolbar_view.add_top_bar(content_header_bar)

        content_page = Adw.NavigationPage.new(content_toolbar_view, "Algorithm Configuration")
        content_page.set_tag("algo_config_view")

        header_bar = Adw.HeaderBar(show_title=False)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self.__setup_row)
        factory.connect("bind", self.__bind_row)

        sidebar = Gtk.ListView.new(algo_config_manager.algorithm_configurations, factory)
        sidebar.add_css_class("navigation-sidebar")

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

        condition = Adw.BreakpointCondition.new_length(Adw.BreakpointConditionLengthType.MAX_WIDTH,
                                                       600, Adw.LengthUnit.PT)
        bpoint = Adw.Breakpoint.new(condition)
        bpoint.add_setter(self.__split_view, "collapsed", True)

        self.set_content(self.__split_view)
        self.add_breakpoint(bpoint)

    @staticmethod
    def __setup_row(factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem) -> None:
        list_item.set_child(AlgoConfigRow())

    @staticmethod
    def __bind_row(factory: Gtk.SignalListItemFactory, list_item: Gtk.ListItem) -> None:
        config = cast(AlgorithmConfiguration, list_item.get_item())
        row = cast(AlgoConfigRow, list_item.get_child())
        row.bind(config)

    def __on_add_clicked(self, button: Gtk.Button) -> None:
        utils.run_coro_with_error_reporting(self.__add_algo_config())

    async def __add_algo_config(self) -> None:
        await self.__manager.create_algorithm_configuration()

    def __on_delete(self, widget: Gtk.Widget, action_name: str,
                    parameter: GLib.Variant | None) -> None:
        if not parameter:
            return

        algo_id = parameter.get_string()
        utils.run_coro_with_error_reporting(self.__delete_algo_config(algo_id))

    async def __delete_algo_config(self, config_id: str) -> None:
        await self.__manager.delete_algorithm_configuration(config_id)
