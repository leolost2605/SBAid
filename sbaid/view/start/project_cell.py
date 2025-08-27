"""This module contains the ProjectCell class."""
import sys
from enum import Enum

import gi

from sbaid.view_model.project import Project
from sbaid.view.i18n import i18n

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GObject, GLib, Gdk, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ProjectCellType(Enum):
    """
    The project property to be shown in the cell.
    """
    NAME = 0
    CREATED_AT = 1
    LAST_OPENED = 2


class ProjectCell(Adw.Bin):
    """
    This class displays a property of a project for use in a column view. It allows itself
    to be recycled for performance.
    """
    __type: ProjectCellType
    __label: Gtk.Label

    __label_binding: GObject.Binding | None = None

    def __init__(self, cell_type: ProjectCellType) -> None:
        super().__init__()
        self.__type = cell_type

        self.__menu_model = Gio.Menu()

        self.__menu = Gtk.PopoverMenu.new_from_model(self.__menu_model)
        self.__menu.set_has_arrow(False)
        self.__menu.set_halign(Gtk.Align.START)

        self.__label = Gtk.Label(xalign=0)

        gesture_click = Gtk.GestureClick(button=0, exclusive=True)
        gesture_click.connect("pressed", self.__on_clicked)

        self.set_child(self.__label)
        self.add_controller(gesture_click)

    def __on_clicked(self, click: Gtk.GestureClick, n_press: int, x: float, y: float) -> None:
        event = click.get_current_event()

        if not event:
            return

        if event.triggers_context_menu():
            click.set_state(Gtk.EventSequenceState.CLAIMED)
            click.reset()

            rect = Gdk.Rectangle()
            rect.x = int(x)
            rect.y = int(y)

            if not self.__menu.get_parent():
                self.__menu.set_parent(self)

            self.__menu.set_pointing_to(rect)
            self.__menu.popup()

    def bind(self, project: Project) -> None:
        """
        Binds the given project to this cell for display.
        :param project: the project to bind
        """
        if self.__label_binding:
            self.__label_binding.unbind()

        match self.__type:
            case ProjectCellType.NAME:
                self.__label_binding = project.bind_property("name", self.__label, "label",
                                                             GObject.BindingFlags.SYNC_CREATE)
            case ProjectCellType.CREATED_AT:
                self.__label_binding = project.bind_property(
                    "created-at", self.__label, "label",
                    GObject.BindingFlags.SYNC_CREATE, self.__date_time_transform_func)
            case ProjectCellType.LAST_OPENED:
                self.__label_binding = project.bind_property(
                    "last-opened", self.__label, "label",
                    GObject.BindingFlags.SYNC_CREATE, self.__date_time_transform_func)

        self.__menu_model.remove_all()
        self.__menu_model.append(i18n._("Rename"), Gio.Action.print_detailed_name(
            "project.rename", GLib.Variant.new_string(project.id)))
        self.__menu_model.append(i18n._("Delete"), Gio.Action.print_detailed_name(
            "project.delete", GLib.Variant.new_string(project.id)))

    @staticmethod
    def __date_time_transform_func(binding: GObject.Binding, date_time: GLib.DateTime) -> str:
        return date_time.format("%x %X")
