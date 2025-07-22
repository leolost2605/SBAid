"""This module represents the SimulationObserver class"""
from gi.repository import GLib, GObject


class SimulationObserver(GObject.GInterface):
    """This class defines the SimulationObserver interface for observing
    the status of a simulation"""

    def update_progress(self, percentage: float) -> None:
        """Notify the progress of the simulation"""

    def finished(self, result_id: str) -> None:
        """Notify when the simulation finishes successfully"""

    def failed(self, error: GLib.Error) -> None:
        """Notify when the simulation failed"""
