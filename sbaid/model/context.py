"""This module defines the Context Class"""
from gi.repository import GObject, Gio
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.results.result_manager import ResultManager


class Context(GObject.GObject):
    """todo"""

    result_manager = GObject.Property(
        type=ResultManager,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    projects = GObject.Property(
        type=Gio.ListModel,
        flags=GObject.ParamFlags.READABLE |
        GObject.ParamFlags.WRITABLE |
        GObject.ParamFlags.CONSTRUCT_ONLY)

    def load(self) -> None:
        """todo"""

    def create_project(self, name: str, sim_type: SimulatorType, simulation_file_path: str,
                       project_file_path: str) -> str:
        """todo"""
        return None

    def delete_project(self, project_id: str) -> None:
        """todo"""
