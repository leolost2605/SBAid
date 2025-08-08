"""This module contains the all projects page."""
import sys

from typing import cast

import gi

from sbaid import common
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


class _RenameDialog(Adw.Dialog):
    __project: Project
    __entry: Gtk.Entry

    def __init__(self, project: Project) -> None:
        super().__init__()

        self.__project = project

        header_bar = Adw.HeaderBar()

        self.__entry = Gtk.Entry(text=project.name, margin_start=12, margin_top=12,
                                 margin_bottom=12, margin_end=12, activates_default=True)

        rename_button = Gtk.Button(label="Rename", margin_start=6, margin_top=6, margin_bottom=6,
                                   margin_end=6, receives_default=True, halign=Gtk.Align.END)
        rename_button.add_css_class("suggested-action")
        rename_button.connect("clicked", self.__on_rename_clicked)

        toolbar_view = Adw.ToolbarView(content=self.__entry)
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.add_bottom_bar(rename_button)

        self.set_child(toolbar_view)
        self.set_title("Rename Project")
        self.set_content_width(300)

    def __on_rename_clicked(self, button: Gtk.Button) -> None:
        self.__project.name = self.__entry.get_text()
        self.close()


class AllProjects(Adw.NavigationPage):
    """
    This class represents the all projects page, where
    all projects that are known to sbaid can be seen and edited.
    """

    def __init__(self, context: Context) -> None:  # pylint: disable=too-many-locals
        super().__init__()
        self.__context = context

        header_bar = Adw.HeaderBar()

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("setup", self.__on_factory_setup, ProjectCellType.NAME)
        name_factory.connect("bind", self.__on_factory_bind)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)
        name_column.set_expand(True)

        last_modified_factory = Gtk.SignalListItemFactory()
        last_modified_factory.connect("setup", self.__on_factory_setup,
                                      ProjectCellType.LAST_MODIFIED)
        last_modified_factory.connect("bind", self.__on_factory_bind)

        last_modified_column = Gtk.ColumnViewColumn.new("Created at", last_modified_factory)

        created_at_factory = Gtk.SignalListItemFactory()
        created_at_factory.connect("setup", self.__on_factory_setup, ProjectCellType.CREATED_AT)
        last_modified_factory.connect("bind", self.__on_factory_bind)

        created_at_column = Gtk.ColumnViewColumn.new("Last Modified", last_modified_factory)

        self.__selection = Gtk.SingleSelection.new(self.__context.projects)

        column_view = Gtk.ColumnView.new(self.__selection)
        column_view.append_column(name_column)
        column_view.append_column(last_modified_column)
        column_view.append_column(created_at_column)
        column_view.connect("activate", self.__on_activate)

        column_view_scrolled = Gtk.ScrolledWindow(child=column_view, propagate_natural_width=True,
                                                  propagate_natural_height=True)

        column_view_frame = Gtk.Frame(child=column_view_scrolled, margin_top=12, margin_bottom=12,
                                      margin_end=12, margin_start=12)

        delete_button = Gtk.Button(label="Delete")
        delete_button.connect("clicked", self.__on_delete)

        rename_button = Gtk.Button(label="Rename", action_name="project.rename")

        button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
        button_box.set_margin_start(12)
        button_box.set_margin_bottom(12)
        button_box.append(delete_button)
        button_box.append(rename_button)

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)
        main_view.set_content(column_view_frame)
        main_view.add_bottom_bar(button_box)

        self.set_child(main_view)
        self.set_title("All Projects")

        self.install_action("project.rename", None, self.__on_rename_project)

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

    async def __delete_project(self, project: Project) -> None:
        await self.__context.delete_project(project.id)

    def __on_delete(self, widget: Gtk.Widget) -> None:
        common.run_coro_in_background(self.__delete_project(
            cast(Project, self.__selection.get_selected_item())))

    def __on_rename_project(self, widget: Gtk.Widget, action_name: str,
                            parameter: GLib.Variant | None) -> None:
        project = cast(Project, self.__selection.get_selected_item())
        if project:
            _RenameDialog(project).present(cast(Adw.Window, self.get_root()))
