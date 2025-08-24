"""This module contains a dialog for renaming something."""
import sys
from typing import Callable, Any

import gi

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class RenameDialog(Adw.Dialog):
    """
    This class represents a dialog shown to the user which allows to rename anything.
    """
    __renamable: Any
    __rename_func: Callable[[Any, str], None]
    __entry: Gtk.Entry

    def __init__(self, old_name: str, renamable: Any,
                 rename_func: Callable[[Any, str], None]) -> None:
        super().__init__()

        self.__renamable = renamable
        self.__rename_func = rename_func

        header_bar = Adw.HeaderBar()

        self.__entry = Gtk.Entry(text=old_name, margin_start=12, margin_top=12,
                                 margin_bottom=12, margin_end=12, activates_default=True)

        rename_button = Gtk.Button(label="Rename", margin_start=6, margin_top=6, margin_bottom=6,
                                   margin_end=6, receives_default=True, halign=Gtk.Align.END)
        rename_button.add_css_class("suggested-action")
        rename_button.connect("clicked", self.__on_rename_clicked)

        toolbar_view = Adw.ToolbarView(content=self.__entry)
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.add_bottom_bar(rename_button)

        self.set_child(toolbar_view)
        self.set_title("Rename")
        self.set_content_width(300)
        self.set_default_widget(rename_button)

    def __on_rename_clicked(self, button: Gtk.Button) -> None:
        self.__rename_func(self.__renamable, self.__entry.get_text())
        self.close()
