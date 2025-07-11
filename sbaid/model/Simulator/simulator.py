from gi.repository import Gio
""""""
from sbaid.common.simulator_type import SimulatorType


class Simulator:
    def __init__(self, simulator_type: SimulatorType):
        self.simulator_type = simulator_type

    def load_file(file: Gio.File) -> None:
        pass

    def create_cross_section(coordinates: Coordinates, type: SimulatorType) -> int:
        # returns position of the new cross section
        return 0

    def remove_cross_section(self, id: str) -> None:
        pass

    def move_cross_section(self, id: str, new_coordinates: Coordinates) -> None:
        pass

    def init_simulation(start_timestamp: DateTime, timespan: TimeSpan) -> None:
        pass

    def continue_simulation(span: int) -> None:
        pass

    def measure(self) -> Simulation.Input:
        return None

    def set_display(self, display: Display) -> None:
        pass

    def stop_simulation(self) -> None:
        pass