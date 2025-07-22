"""This module defines the Project class."""

from gi.repository import GObject, GLib
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.simulation_manager import SimulationManager
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import (
    AlgorithmConfigurationManager)
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.network.network import Network


class Project(GObject.GObject):
    """todo"""

    id = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    name = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    simulator_type = GObject.Property(
        type=SimulatorType,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    project_file_path = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    simulation_file_path = GObject.Property(
        type=str,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    created_at = GObject.Property(
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    last_modified = GObject.Property(
        type=GLib.DateTime,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT)

    simulator = GObject.Property(
        type=Simulator,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    network = GObject.Property(
        type=Network,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    algorithm_configuration_manager = GObject.Property(
        type=AlgorithmConfigurationManager,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def __init__(self, project_id: str, sim_type: SimulatorType, simulation_file_path: str,
                 project_file_path: str) -> None:
        """todo"""
        super().__init__(id=project_id, simulator_type=sim_type,
                         simulation_file_path=simulation_file_path,
                         project_file_path=project_file_path)

    def load(self) -> None:
        """todo"""

    def start_simulation(self, observer: SimulationObserver) -> SimulationManager:
        """todo"""
        return None

    def load_from_db(self) -> None:
        """todo: check privacy"""
