"""This module contains the all projects page."""
import sys

from typing import cast, Any

import gi

from sbaid.view import utils
from sbaid.view.common.rename_dialog import RenameDialog
from sbaid.view.start.project_cell import ProjectCellType, ProjectCell
from sbaid.view_model.context import Context

from sbaid.view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AllProjects(Adw.NavigationPage):
    """
    This class represents the all projects page, where
    all projects that are known to sbaid can be seen and edited.
    """

    def __init__(self, context: Context) -> None:  # pylint: disable=too-many-locals
        super().__init__()
        self.__context = context

        header_bar = Adw.HeaderBar()

        column_view = Gtk.ColumnView()
        sorter = column_view.get_sorter()
        sort_model = Gtk.SortListModel.new(self.__context.projects, sorter)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self.__on_factory_setup, ProjectCellType.NAME)
        name_factory.connect("bind", self.__on_factory_bind)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)
        name_column.set_expand(True)
        name_sorter = Gtk.CustomSorter.new(self.__name_sort_func)
        name_column.set_sorter(name_sorter)

        last_opened_factory = Gtk.SignalListItemFactory()
        last_opened_factory.connect("setup", self.__on_factory_setup, ProjectCellType.LAST_OPENED)
        last_opened_factory.connect("bind", self.__on_factory_bind)

        last_opened_column = Gtk.ColumnViewColumn.new("Last Opened", last_opened_factory)
        last_opened_sorter = Gtk.CustomSorter.new(self.__last_opened_sort_func)
        last_opened_column.set_sorter(last_opened_sorter)

        created_at_factory = Gtk.SignalListItemFactory()
        created_at_factory.connect("setup", self.__on_factory_setup, ProjectCellType.CREATED_AT)
        created_at_factory.connect("bind", self.__on_factory_bind)

        created_at_column = Gtk.ColumnViewColumn.new("Created at", last_opened_factory)
        created_at_sorter = Gtk.CustomSorter.new(self.__created_at_sort_func)
        created_at_column.set_sorter(created_at_sorter)

        self.__selection = Gtk.NoSelection.new(sort_model)

        column_view.set_model(self.__selection)
        column_view.set_single_click_activate(True)
        column_view.append_column(name_column)
        column_view.append_column(last_opened_column)
        column_view.append_column(created_at_column)
        column_view.connect("activate", self.__on_activate)

        column_view_scrolled = Gtk.ScrolledWindow(child=column_view, propagate_natural_width=True,
                                                  propagate_natural_height=True)

        column_view_frame = Gtk.Frame(child=column_view_scrolled, margin_top=12, margin_bottom=12,
                                      margin_end=12, margin_start=12)

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(column_view_frame)

        self.set_child(main_view)
        self.set_title("All Projects")

        self.install_action("project.delete", "s", self.__on_delete)
        self.install_action("project.rename", "s", self.__on_rename_project)

    @staticmethod
    def __on_factory_setup(factory: Gtk.SignalListItemFactory,
                           list_item: Gtk.ColumnViewCell, cell_type: ProjectCellType) -> None:
        list_item.set_child(ProjectCell(cell_type))

    @staticmethod
    def __on_factory_bind(factory: Gtk.SignalListItemFactory,
                          list_item: Gtk.ColumnViewCell) -> None:
        project = cast(Project, list_item.get_item())
        cell = cast(ProjectCell, list_item.get_child())
        cell.bind(project)

    def __on_activate(self, view: Gtk.ColumnView, pos: int) -> None:
        model = view.get_model()
        if model:
            project = cast(Project, model.get_item(pos))  # type: ignore
            self.activate_action("win.open-project", GLib.Variant.new_string(project.id))

    def __get_project_from_param(self, parameter: GLib.Variant | None) -> Project | None:
        if not parameter:
            return None

        project_id = parameter.get_string()

        if not project_id:
            return None

        for p in self.__context.projects:
            project = cast(Project, p)
            if project.id == project_id:
                return project

        return None

    def __on_delete(self, widget: Gtk.Widget, action_name: str,
                    parameter: GLib.Variant | None) -> None:
        project = self.__get_project_from_param(parameter)
        if project:
            utils.run_coro_with_error_reporting(self.__context.delete_project(project.id))

    def __on_rename_project(self, widget: Gtk.Widget, action_name: str,
                            parameter: GLib.Variant | None) -> None:
        project = self.__get_project_from_param(parameter)
        if project:
            RenameDialog(project.name, project, self.__project_rename_func).present(
                cast(Adw.Window, self.get_root()))

    @staticmethod
    def __project_rename_func(project: Project, new_name: str) -> None:
        project.name = new_name

    def __name_sort_func(self, project1: Project, project2: Project, data: Any) -> int:
        if project1.name < project2.name:
            return 1
        if project1.name > project2.name:
            return -1
        return 0

    def __created_at_sort_func(self, project1: Project, project2: Project, data: Any) -> int:
        return project1.created_at.compare(project2.created_at)

    def __last_opened_sort_func(self, project1: Project, project2: Project, data: Any) -> int:
        return project1.last_opened.compare(project2.last_opened)
