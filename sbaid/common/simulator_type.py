"""this module defines the SimulatorType class"""
class SimulatorType:
    """This class represents a type of simulator.
    Attributes:
        simulator_type_id (str): The unique identifier for the simulator type.
        name (str): The name of the simulator type.
    """

    def __init__(self, simulator_type_id: str, name: str) -> None:
        """Initialize the simulator type with an id and a name."""
        self.simulator_type_id = simulator_type_id
        self.name = name