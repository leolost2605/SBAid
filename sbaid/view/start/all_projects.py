"""This module contains the all projects page."""
import sys
from typing import cast, Any

import gi

import sbaid.common
from sbaid.view_model.context import Context

from babel.dates import format_datetime
import datetime

from view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AllProjects(Adw.NavigationPage):
    """This class represents the all projects page, where
    all projects that are known to sbaid can be seen and edited."""

    def on_factory_setup(self, factory, list_item):
        label = Gtk.Label(xalign=0)
        list_item.set_child(label)
        self.right_click.connect("pressed", self.__on_right_click)
        # list_item.add_controller(right_click)


    def on_factory_bind(self, factory, list_item, get_text_func):
        item = list_item.get_item()
        label = list_item.get_child()
        label.set_text(get_text_func(item))


    def __init__(self, context: Context) -> None:
        super().__init__()
        self.__context = context

        self.right_click = Gtk.GestureClick(button=0)
        self.right_click.set_button(0)

        name_factory = Gtk.SignalListItemFactory()
        name_factory.connect("bind", self.on_factory_bind, lambda obj: obj.name)
        name_factory.connect("setup", self.on_factory_setup)

        name_column = Gtk.ColumnViewColumn.new("Name", name_factory)
        sorter = Gtk.StringSorter()
        expression = Gtk.PropertyExpression.new(Project, None, "name")
        sorter.set_expression(expression)

        name_column.set_sorter(sorter)

        # name_column.set_sorter(Gtk.CustomSorter.new(self.__sort_name_func))

        last_modified_factory = Gtk.SignalListItemFactory()
        last_modified_factory.connect("bind", self.on_factory_bind,
                                      lambda obj: format_datetime(
                                          datetime.datetime.fromisoformat(
                                              obj.last_modified.format_iso8601()),
                                          format="medium", locale='de'))
        last_modified_factory.connect("setup", self.on_factory_setup)

        last_modified_column = Gtk.ColumnViewColumn.new("Created at", last_modified_factory)

        created_at_factory = Gtk.SignalListItemFactory()
        created_at_factory.connect("bind", self.on_factory_bind,
                                      lambda obj: format_datetime(
                                          datetime.datetime.fromisoformat(
                                              obj.created_at.format_iso8601()),
                                          format="medium", locale='de'))
        created_at_factory.connect("setup", self.on_factory_setup)

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
        delete_button.connect("clicked", self.__on_delete)

        open_button = Gtk.Button(label="Open")
        open_button.set_action_name("win.open-project")
        project = self.selection.get_selected_item()
        open_button.set_action_target_value(GLib.Variant.new_string(project.id))

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.append(delete_button)
        button_box.append(open_button)

        header_bar = Adw.HeaderBar()
        main_view = Adw.ToolbarView()

        main_view.add_top_bar(header_bar)
        main_view.add_bottom_bar(button_box)

        main_view.set_content(self.column_view)

        self.set_child(main_view)
        self.set_title("All Projects")
    async def __delete_project(self, project: Project):
        await self.__context.delete_project(project.id)

    def __on_delete(self, widget: Gtk.Widget):
        sbaid.common.run_coro_in_background(self.__delete_project(
            cast(Project, self.selection.get_selected_item())))



    def __on_right_click(self, gesture, n_press, x, y):
        # is right click
        if gesture.get_current_button() == 3:

            menu = Gio.Menu()
            menu.append("test")

            right_click_menu = Gtk.PopoverMenu()
            right_click_menu.set_menu_model(menu)
            right_click_menu.set_parent(self)
            print("debug")
            right_click_menu.popup()

    # def __sort_name_func(self, project1: Any, project2: Any, data: Any) -> int | None:
    #     if not isinstance(project1, Project) or not isinstance(project2, Project):
    #         return None
    #     if project1.name > project2.name:
    #         return 1
    #     if project1.name < project2.name:
    #         return -1
    #     return 0
