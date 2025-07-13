"""this module defines the SimulatorType class"""
from gi.repository import GObject


class SimulatorType(GObject.GObject):
    """TODO"""
    simulator_type_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.CONSTRUCT)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE | GObject.ParamFlags.WRITABLE)

    def __init__(self, simulator_type_id: str, name: str) -> None:
        """Initialize the simulator type with an id and a name."""
        self.simulator_type_id = simulator_type_id
        self.name = name
