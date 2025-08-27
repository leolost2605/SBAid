"""
This module contains the simulation running page.
"""

import sys

import gi

from sbaid.view import utils
from sbaid.view_model.simulation import Simulation
from sbaid.view.i18n import i18n

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gtk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class SimulationRunningPage(Adw.NavigationPage):
    """
    This page is shown while a simulation is running. It allows to cancel the simulation
    and provides progress information.
    """

    __simulation: Simulation
    __status_page: Adw.StatusPage

    def __init__(self, simulation: Simulation):
        super().__init__()

        self.__simulation = simulation

        header_bar = Adw.HeaderBar()

        self.__progress_bar = Gtk.ProgressBar()
        self.__progress_bar.set_halign(Gtk.Align.CENTER)

        cancel_button = Gtk.Button.new_with_label(i18n._("Cancel"))
        cancel_button.set_halign(Gtk.Align.CENTER)
        cancel_button.add_css_class("destructive-action")
        cancel_button.connect("clicked", self.__on_cancel_clicked)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        box.append(self.__progress_bar)
        box.append(cancel_button)

        self.__status_page = Adw.StatusPage()
        self.__status_page.set_title(i18n._("Simulating…"))
        self.__status_page.set_description(i18n._("A Simulation is ongoing."))
        self.__status_page.set_child(box)

        toolbar_view = Adw.ToolbarView()
        toolbar_view.add_top_bar(header_bar)
        toolbar_view.set_content(self.__status_page)

        self.set_child(toolbar_view)
        self.set_title(i18n._("Simulation"))
        self.set_can_pop(False)

        simulation.connect("progressed", self.__on_progressed)
        simulation.connect("finished", self.__on_finished)
        simulation.connect("failed", self.__on_failed)

    def __on_progressed(self, simulation: Simulation, progress: float) -> None:
        self.__progress_bar.set_fraction(progress)

    def __on_finished(self, simulation: Simulation, result_id: str) -> None:
        self.set_can_pop(True)

        open_result_button = Gtk.Button.new_with_label(i18n._("Show Result"))
        open_result_button.add_css_class("suggested-action")
        open_result_button.add_css_class("pill")
        open_result_button.set_halign(Gtk.Align.CENTER)
        open_result_button.set_action_name("win.export-result")
        open_result_button.set_action_target_value(GLib.Variant.new_string(result_id))

        self.__status_page.set_title(i18n._("Simulation Completed"))
        self.__status_page.set_description(i18n._("The Simulation was completed successfully. "
                                                  "You can now view the result."))
        self.__status_page.set_child(open_result_button)

    def __on_failed(self, simulation: Simulation, error: GLib.Error) -> None:
        self.set_can_pop(True)

        self.__status_page.set_title(i18n._("Simulation Failed"))
        self.__status_page.set_description(error.message)
        self.__status_page.set_child(None)

    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.set_can_pop(True)

        button.set_sensitive(False)
        utils.run_coro_with_error_reporting(self.__simulation.cancel())
        # TODO: Auto navigate back?
