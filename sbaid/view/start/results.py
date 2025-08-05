"""This module contains the results page."""
import sys

import gi

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Results(Adw.NavigationPage):
    """This class represents the results page which is used to access results."""
    def __init__(self) -> None:
        super().__init__()
        header_bar = Adw.HeaderBar()

        main_view = Adw.ToolbarView()
        main_view.add_top_bar(header_bar)

        self.set_child(main_view)
        self.set_title("Results")
