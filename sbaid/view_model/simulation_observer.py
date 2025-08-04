"""
This module contains the simulation observer interface implementation.
"""

from gi.repository import GLib, GObject

from sbaid.model.simulation_observer import SimulationObserver as ModelSimulationObserver


class SimulationObserver(ModelSimulationObserver):
    """
    Implements the SimulationObserver interface. Takes the information
    and emits corresponding signals. This implementation just takes the information
    and emits the signals to hide the underlying public methods. See also simulation
    """

    __gsignals__ = {
        "progressed": (GObject.SIGNAL_RUN_FIRST, None, (float,)),
        "finished": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        "failed": (GObject.SIGNAL_RUN_FIRST, None, (GObject.Error,)),
    }

    def update_progress(self, percentage: float) -> None:
        """
        Emits the progressed signal with the given percentage.
        :param percentage: the current progress of the simulation
        """
        self.emit("progressed", percentage)

    def finished(self, result_id: str) -> None:
        """
        Emits the finished signal with the given result id.
        :param result_id: the id of the result of the simulation
        """
        self.emit("finished", result_id)

    def failed(self, error: GLib.Error) -> None:
        """
        Emits the failed signal with the given error.
        :param error: the error that caused the simulation to fail
        """
        self.emit("failed", error)
