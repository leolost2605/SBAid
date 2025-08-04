"""
This module contains the welcome page.
"""
import sys
import gi

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class WelcomePage(Adw.NavigationPage):
    """
    This page is the first page displayed when opening sbaid.
    It welcomes the user and provides a list of recently used project as well
    as allowing to view all projects and the result view.
    """

    def __init__(self) -> None:
        super().__init__()

        header_bar = Adw.HeaderBar.new()  # pylint: disable=no-value-for-parameter

        main_view = Adw.ToolbarView.new()  # pylint: disable=no-value-for-parameter
        main_view.add_top_bar(header_bar)

        self.set_child(main_view)
        self.set_title("Welcome Page")
