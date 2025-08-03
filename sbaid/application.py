"""
This module contains the main application class that is initialized in the SBAid main method.
"""

import sys
import gi

from sbaid.model.context import Context as ModelContext

try:
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Application(Gtk.Application):
    """
    This class contains the main application that handles running the main loop
    and the lifetime management of the process. It also creates the model context and view
    model context, starts loading them and opens the window.
    """

    __model_context: ModelContext
    __window: Gtk.Window | None

    def __init__(self) -> None:
        super().__init__()
        self.__window = None

    def do_startup(self) -> None:
        self.__model_context = ModelContext()

    def do_activate(self, *args, **kwargs) -> None:
        if not self.__window:
            self.__window = Gtk.Window.new()

        self.__window.present()
