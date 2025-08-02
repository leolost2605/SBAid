"""
This module contains the Simulation class responsible for managing a running simulation.
"""

from gi.repository import GObject

from sbaid.model.simulation_manager import SimulationManager as ModelSimulationManager
from sbaid.view_model.simulation_observer import SimulationObserver


class Simulation(GObject.Object):
    """
    Represents a running simulation. Allows to receive information about and control
    the simulation.
    """

    __gsignals__ = {
        "progressed": (GObject.SIGNAL_RUN_FIRST, None, (float,)),
        "finished": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        "failed": (GObject.SIGNAL_RUN_FIRST, None, (GObject.Error,)),
    }

    __manager: ModelSimulationManager

    def __init__(self, manager: ModelSimulationManager, observer: SimulationObserver):
        super().__init__()
        self.__manager = manager
        observer.connect("progressed", self.__on_progressed)
        observer.connect("finished", self.__on_finished)
        observer.connect("failed", self.__on_failed)

    def __on_progressed(self, observer: SimulationObserver, progress: float) -> None:
        self.emit("progressed", progress)

    def __on_finished(self, observer: SimulationObserver, result_id: str) -> None:
        self.emit("finished", result_id)

    def __on_failed(self, observer: SimulationObserver, error: GObject.Error) -> None:
        self.emit("failed", error)

    def cancel(self) -> None:
        """
        Cancels the simulation.
        """
        self.__manager.cancel()
