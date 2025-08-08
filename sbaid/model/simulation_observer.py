"""This module represents the SimulationObserver class"""
from gi.repository import GLib, GObject


class SimulationObserver(GObject.GObject):
    """This class defines the SimulationObserver interface for observing
    the status of a simulation"""

    def update_progress(self, percentage: float) -> None:
        """Notify the progress of the simulation about the current
        progress with percentage between 0.0 and 1.0."""

    def finished(self, result_id: str) -> None:
        """Notify when the simulation finishes successfully and gives
        the id of the result that was created in the process"""

    def failed(self, error: GLib.Error) -> None:
        """Notify when the simulation failed and passes an error with
        further information."""
