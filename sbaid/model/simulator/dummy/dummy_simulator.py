"""This module contains the DummySimulator class."""
import asyncio

from gi.repository import GObject, Gio

import csv

from sbaid.common.simulator_type import SimulatorType
from sbaid.common.vehicle_type import VehicleType
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.simulation.input import Input
from sbaid.common.coordinate import Coordinate
from sbaid.model.simulation.display import Display
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class DummySimulator(Simulator):
    """TODO"""

    _type: SimulatorType
    _cross_sections: Gio.ListModel

    _sequence: dict[int, Input]
    _pointer: int

    def __init__(self) -> None:
        self._type = SimulatorType("dummy.csv", "CSV Dummy")
        self._cross_sections = Gio.ListStore.new(SimulatorCrossSection)
        self._sequence = {}
        self._pointer = 0

    @GObject.Property(type=SimulatorType)
    def type(self) -> SimulatorType:
        """TODO"""
        return self._type

    @GObject.Property(type=Gio.ListModel)
    def cross_sections(self) -> Gio.ListModel:
        """TODO"""
        return self._cross_sections


    async def load_file(self, file: Gio.File) -> None:
        """TODO"""
        with open(file.get_path()) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=",")
            first_line = next(csv_reader)
            if first_line != {'AVG_SPEED': '125.0', 'TRAFFIC_VOL': '12'}:
                return
            temp_sequence = {}
            counter = 0
            for line in csv_reader:
                temp_sequence[counter] = line
                counter += 1

            counter = 0
            for line in temp_sequence.values():
                new_input = Input()
                vehicle_amount = line.get("TRAFFIC_VOL")
                for i in vehicle_amount:
                    new_input.add_vehicle_info("cross_section", 0, VehicleType.CAR,
                                               float(line.get("AVG_SPEED")))
                self._sequence[counter] = new_input
                counter += 1

            print(self._sequence.values())


    async def create_cross_section(self, coordinate: Coordinate,
                                   cross_section_type: CrossSectionType) -> int:
        """TODO"""
        return 0

    async def remove_cross_section(self, cross_section_id: str) -> None:
        """TODO"""

    async def move_cross_section(self, cross_section_id: str, new_position: Coordinate) -> None:
        """TODO"""

    async def init_simulation(self) -> tuple[int, int]:
        return 0, len(self._sequence)

    async def continue_simulation(self, span: int) -> None:
        """TODO"""
        self._pointer = self._pointer + span

    async def measure(self) -> Input:
        return self._sequence.get(self._pointer)

    async def set_display(self, display: Display) -> None:
        """TODO"""

    async def stop_simulation(self) -> None:
        """TODO"""
        self._pointer = 0

sim = DummySimulator()
file = Gio.File.new_for_path("test.csv")
asyncio.run(sim.load_file(file))