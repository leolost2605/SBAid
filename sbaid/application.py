"""
This module contains the main application class that is initialized in the SBAid main method.
"""

import sys
from typing import Any

import gi

from sbaid import common
from sbaid.model.context import Context as ModelContext
from sbaid.view_model.context import Context
from sbaid.view.main_window import MainWindow

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Gtk, Adw
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class Application(Adw.Application):
    """
    This class contains the main application that handles running the main loop
    and the lifetime management of the process. It also creates the model context and view
    model context, starts loading them and opens the window.
    """

    __view_model_context: Context
    __window: Gtk.Window | None

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            *args,
            application_id="io.github.leolost2605.sbaid",  # type: ignore
            **kwargs,
        )

        self.__window = None

    def do_startup(self, *args: Any, **kwargs: Any) -> None:
        Adw.Application.do_startup(self)

        model_context = ModelContext()
        self.__view_model_context = Context(model_context)
        common.run_coro_in_background(model_context.load())

        self.__view_model_context = Context(ModelContext())
        common.run_coro_in_background(self.__view_model_context.load())

    def do_activate(self, *args: Any, **kwargs: Any) -> None:
        if not self.__window:
            self.__window = MainWindow(self.__view_model_context, application=self)

        self.__window.present()
