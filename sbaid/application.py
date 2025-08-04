"""
This module contains the main application class that is initialized in the SBAid main method.
"""

import sys
import gi

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)

from sbaid.model.context import Context as ModelContext
from sbaid.view.main_window import MainWindow, Context


class Application(Adw.Application):
    """
    This class contains the main application that handles running the main loop
    and the lifetime management of the process. It also creates the model context and view
    model context, starts loading them and opens the window.
    """

    __view_model_context: Context
    __window: Gtk.Window | None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            application_id="io.github.leolost2605.sbaid",
            **kwargs
        )
        self.__window = None

    def do_startup(self) -> None:  # pylint: disable=arguments-differ
        Adw.Application.do_startup(self)

        ModelContext()
        self.__view_model_context = Context()

    def do_activate(self, *args, **kwargs) -> None:
        if not self.__window:
            self.__window = MainWindow(self.__view_model_context, application=self)

        self.__window.present()
