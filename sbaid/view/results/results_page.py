"""This module contains the results page."""
import gi
import sys
from sbaid.view_model.context import Context

#from sbaid.view_model.results.result

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw, GLib
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class ResultsPage(Adw.NavigationPage):
    """This class contains the results page, containing the results to all
    simulations ran on SBAid."""


    def __init__(self, context: Context) -> None:
        super().__init__()
        self.__context = context
