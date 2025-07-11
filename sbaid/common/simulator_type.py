"""this module defines the SimulatorType class"""
from gi.repository import GObject

class SimulatorType(GObject.GObject):
    """This class represents a type of simulator.
    Attributes:
        simulator_type_id (str): The unique identifier for the simulator type.
        name (str): The name of the simulator type.
    """
    simulator_type_id = GObject.Property(name=str)
    name = GObject.Property(name=str)

    def __init__(self, simulator_type_id: str, name: str) -> None:
        """Initialize the simulator type with an id and a name."""
        self.simulator_type_id = simulator_type_id
        self.name = name
