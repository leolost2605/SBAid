"""This module defines the SimulatorType class"""
from gi.repository import GObject


class SimulatorType(GObject.GObject):
    """TODO"""
    simulator_type_id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)
    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    def __init__(self, simulator_type_id: str, name: str) -> None:
        """TODO"""
        super().__init__(simulator_type_id=simulator_type_id, name=name)
