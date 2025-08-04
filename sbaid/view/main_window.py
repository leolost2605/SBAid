"""
This module contains the main window of sbaid.
"""

import sys
import gi

from sbaid.view.start.welcome_page import WelcomePage

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Context:
    """Placeholder"""


class MainWindow(Adw.ApplicationWindow):
    """
    This class contains the main window of the application.
    It handles managing the pages and provides actions for opening new ones.
    """
    __context: Context
    __nav_view: Adw.NavigationView

    def __init__(self, context: Context, **kwargs):
        super().__init__(**kwargs)
        self.__context = context  # pylint: disable=unused-private-member

        welcome_page = WelcomePage()

        self.__nav_view = Adw.NavigationView.new()  # pylint: disable=no-value-for-parameter
        self.__nav_view.add(welcome_page)

        self.set_content(self.__nav_view)

        # Add actions
        open_project_action = Gio.SimpleAction.new('open-project', GLib.VariantType.new("s"))
        open_project_action.connect("activate", self.__on_open_project)

    def __on_open_project(self, action: Gio.SimpleAction, param: GLib.Variant) -> None:
        pass
        # project = self.__context.get_project_by_id(param.get_string())
        # self.__nav_view.push(ProjectMainPage(project))
