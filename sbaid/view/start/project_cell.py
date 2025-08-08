"""This module contains the ProjectCell class."""
import sys
from enum import Enum

import gi

from sbaid.view_model.project import Project

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GObject, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ProjectCellType(Enum):
    """
    The project property to be shown in the cell.
    """
    NAME = 0
    CREATED_AT = 1
    LAST_MODIFIED = 2


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
        self.__label = Gtk.Label(xalign=0)
        self.set_child(self.__label)

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
            case ProjectCellType.LAST_MODIFIED:
                self.__label_binding = project.bind_property(
                    "last-modified", self.__label, "label",
                    GObject.BindingFlags.SYNC_CREATE, self.__date_time_transform_func)

    @staticmethod
    def __date_time_transform_func(binding: GObject.Binding, date_time: GLib.DateTime) -> str:
        return date_time.format("%x %X")
