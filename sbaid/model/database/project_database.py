"""TODO"""
from typing import Optional

from gi.repository.GObject import GInterface
from gi.repository.GLib import Variant
from gi.repository.GLib import DateTime
from gi.repository.Gio import File


class ProjectDatabase(GInterface):
    """TODO"""

    def open(self, file: File) -> None:
        """TODO"""

    def get_created_at(self) -> DateTime:
        """TODO"""
        return DateTime()

    def get_last_modified(self) -> DateTime:
        """TODO"""
        return DateTime()

    def set_last_modified(self, new_last_modified: DateTime) -> None:
        """TODO"""

    def get_project_name(self) -> str:
        """TODO"""
        return ""

    def set_project_name(self, name: str) -> None:
        """TODO"""

    def get_cross_section_name(self, cross_section_id: str) -> str:
        """TODO"""
        return ""

    def set_cross_section_name(self, name: str) -> None:
        """TODO"""
        return ""

    def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return ""

    def set_algorithm_configuration_name(self, name: str) -> None:
        """TODO"""

    def get_algorithm_configuration(self, algorithm_configuration_id: str) \
            -> tuple[str, int, int, str]:
        """TODO"""
        return "", 0, 0, ""

    def get_all_algorithm_configuration_ids(self) -> list[str]:
        """TODO"""
        return []

    def get_selected_algorithm_configuration_id(self) -> str:
        """TODO"""
        return ""

    def set_selected_algorithm_configuration_id(self, configuration_id: str) -> None:
        """TODO"""

    def get_display_interval(self, algorithm_configuration_id: str) -> int:
        """TODO"""
        return 0

    def set_display_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """TODO"""

    def get_evaluation_interval(self, algorithm_configuration_id: str) -> int:
        """TODO"""
        return 0

    def set_evaluation_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """TODO"""

    def get_script_path(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return ""

    def set_script_path(self, algorithm_configuration_id: str, path: str) -> None:
        """TODO"""

    def get_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                            cross_section_id: Optional[str]) -> str:
        """TODO"""
        return ""

    def set_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                            cross_section_id: Optional[str], parameter_value: Variant) -> None:
        """TODO"""
