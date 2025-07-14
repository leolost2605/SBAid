"""This module represents the SimulationObserver class"""
from abc import ABC
from gi.repository import GLib


class SimulationObserver(ABC):
    """todo"""

    def __init__(self) -> None:
        """todo"""

    def update_progress(self, percentage: float) -> None:
        """todo"""

    def finished(self, result_id: str) -> None:
        """todo"""

    def failed(self, error: GLib.Error) -> None:
        """todo"""
