"""this module defines the SimulatorType class"""
from gi.repository import GObject


class SimulatorType(GObject.GObject):
    """TODO"""
    simulator_type_id = GObject.Property(name=str,
                                         flags=GObject.PARAM_READABLE)
    name = GObject.Property(name=str, flags=GObject.PARAM_READWRITE)

    def __init__(self, simulator_type_id: str, name: str) -> None:
        """Initialize the simulator type with an id and a name."""
        self.simulator_type_id = simulator_type_id
        self.name = name
