"""
This module contains the class used to choose how to add new cross sections.
"""

import sys
from typing import cast

import gi

from sbaid.view import utils
from sbaid.view.main_page.add_new_cross_section_dialog import AddNewCrossSectionDialog
from sbaid.view_model.network.network import Network
from sbaid.common.i18n import i18n


try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AddNewCrossSectionListPopover(Gtk.Popover):
    """
    Popover used to choose how to add new cross sections.
    """

    __network: Network

    def __init__(self, network: Network) -> None:
        super().__init__()
        self.__network = network

        manual_button = Gtk.Button.new_with_label(i18n._("Manual..."))
        manual_button.connect("clicked", self.__on_manual_clicked)

        import_button = Gtk.Button.new_with_label(i18n._("Import..."))
        import_button.connect("clicked", self.__on_import_clicked)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 3)
        box.append(manual_button)
        box.append(import_button)

        self.set_child(box)

    def __on_manual_clicked(self, button: Gtk.Button) -> None:
        self.popdown()
        dialog = AddNewCrossSectionDialog(self.__network)

        parent = self.get_parent()
        assert parent
        dialog.present(cast(Gtk.Window, parent.get_root()))

    def __on_import_clicked(self, button: Gtk.Button) -> None:
        self.popdown()
        utils.run_coro_with_error_reporting(self.__collect_import_file())

    async def __collect_import_file(self) -> None:
        dialog = Gtk.FileDialog()

        try:
            file = await dialog.open(self.get_root())  # type: ignore
        except Exception as e:  # pylint: disable=broad-exception-caught
            msg = i18n._("Failed to allow the user to choose a file: ")
            print(msg, e)
            return

        if file is None:
            return

        await self.__network.import_cross_sections(file)
