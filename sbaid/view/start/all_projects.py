"""This module contains the all projects page."""
import sys
# import datetime

from typing import cast, Any, Callable

import gi

# from babel.dates import format_datetime
import sbaid.common
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
    """This class represents the all projects page, where
    all projects that are known to sbaid can be seen and edited."""

    def __init__(self, context: Context) -> None:
        super().__init__()
        self.__context = context

        self.right_click = Gtk.GestureClick(button=0)
        self.right_click.set_button(0)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("bind", self.__on_factory_bind, lambda obj: obj.name)
        name_factory.connect("setup", self.__on_factory_setup)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)

        last_modified_factory = Gtk.SignalListItemFactory()
        # last_modified_factory.connect("bind", self.on_factory_bind,
        #                               lambda obj: format_datetime(
        #                                   datetime.datetime.fromisoformat(
        #                                       obj.last_modified.format_iso8601()),
        #                                   format="medium", locale='de'))
        last_modified_factory.connect("bind", self.__on_factory_bind,
                                      lambda obj: obj.last_modified.format_iso8601())
        last_modified_factory.connect("setup", self.__on_factory_setup)

        last_modified_column = Gtk.ColumnViewColumn.new("Created at", last_modified_factory)

        created_at_factory = Gtk.SignalListItemFactory()
        # created_at_factory.connect("bind", self.on_factory_bind,
        #                            lambda obj: format_datetime(
        #                                datetime.datetime.fromisoformat(
        #                                    obj.created_at.format_iso8601()),
        #                                format="medium", locale='de'))
        last_modified_factory.connect("bind", self.__on_factory_bind,
                                      lambda obj: obj.last_modified.format_iso8601())
        created_at_factory.connect("setup", self.__on_factory_setup)

        created_at_column = Gtk.ColumnViewColumn.new("Last Modified", last_modified_factory)

        self.selection = Gtk.SingleSelection()
        self.selection.set_model(self.__context.projects)

        # Create the column view and set the model
        self.column_view = Gtk.ColumnView()
        self.column_view.set_model(self.selection)

        self.column_view.append_column(name_column)
        self.column_view.append_column(last_modified_column)
        self.column_view.append_column(created_at_column)

        self.column_view.add_controller(self.right_click)

        delete_button = Gtk.Button(label="Delete")
        open_button = Gtk.Button(label="Open")
        project = self.selection.get_selected_item()
        if self.selection.get_selected_item():
            delete_button.connect("clicked", self.__on_delete)

            open_button.set_action_name("win.open-project")
            open_button.set_action_target_value(
                GLib.Variant.new_string(project.id))  # type: ignore

        rename_button = Gtk.Button(label="Rename", action_name="project.rename")

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.append(delete_button)
        button_box.append(open_button)
        button_box.append(rename_button)

        header_bar = Adw.HeaderBar()
        main_view = Adw.ToolbarView()

        main_view.add_top_bar(header_bar)
        main_view.add_bottom_bar(button_box)

        main_view.set_content(self.column_view)

        self.set_child(main_view)
        self.set_title("All Projects")

        self.install_action("project.rename", None, self.__on_rename_project)

    def __on_factory_setup(self, factory: Any, list_item: Gtk.ColumnViewCell) -> None:
        label = Gtk.Label(xalign=0)
        list_item.set_child(label)

    def __on_factory_bind(self, factory: Any, list_item: Gtk.ColumnViewCell,
                          get_text_func: Callable[[Any], str]) -> None:
        item = list_item.get_item()
        label = list_item.get_child()
        label.set_text(get_text_func(item))  # type: ignore

    async def __delete_project(self, project: Project) -> None:
        await self.__context.delete_project(project.id)

    def __on_delete(self, widget: Gtk.Widget) -> None:
        sbaid.common.run_coro_in_background(self.__delete_project(
            cast(Project, self.selection.get_selected_item())))

    def __on_rename_project(self, widget: Gtk.Widget, action_name: str,
                            parameter: GLib.Variant | None) -> None:
        project = cast(Project, self.selection.get_selected_item())
        if project:
            _RenameDialog(project).present(cast(Adw.Window, self.get_root()))
