"""This module represents the SimulationObserver class"""
from gi.repository import GLib, GObject


class SimulationObserver(GObject.GInterface):
    """todo"""

    def update_progress(self, percentage: float) -> None:
        """todo"""

    def finished(self, result_id: str) -> None:
        """todo"""

    def failed(self, error: GLib.Error) -> None:
        """todo"""
