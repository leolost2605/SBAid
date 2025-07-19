"""TODO"""
from gi.repository import GLib, Gio

from sbaid.model.database.project_database import ProjectDatabase


class ProjectSQLite(ProjectDatabase):
    """TODO"""

    async def open(self, file: Gio.File) -> None:
        """TODO"""

    async def get_created_at(self) -> GLib.DateTime:
        """TODO"""
        return None

    async def get_last_modified(self) -> GLib.DateTime:
        """TODO"""
        return None

    async def set_last_modified(self, new_last_modified: GLib.DateTime) -> None:
        """TODO"""

    async def get_project_name(self) -> str:
        """TODO"""
        return ""

    async def set_project_name(self, name: str) -> None:
        """TODO"""

    async def get_cross_section_name(self, cross_section_id: str) -> str:
        """TODO"""
        return ""

    async def set_cross_section_name(self, name: str) -> None:
        """TODO"""

    async def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return ""

    async def set_algorithm_configuration_name(self, name: str) -> None:
        """TODO"""

    async def get_algorithm_configuration(self, algorithm_configuration_id: str)\
            -> tuple[str, int, int, str]:
        """TODO"""
        return "", 0, 0, ""

    async def get_all_algorithm_configuration_ids(self) -> list[str]:
        """TODO"""
        return []

    async def get_selected_algorithm_configuration_id(self) -> str:
        """TODO"""
        return ""

    async def set_selected_algorithm_configuration_id(self, configuration_id: str) -> None:
        """TODO"""

    async def get_display_interval(self, algorithm_configuration_id: str) -> int:
        """TODO"""
        return 0

    async def set_display_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """TODO"""

    async def get_evaluation_interval(self, algorithm_configuration_id: str) -> int:
        """TODO"""
        return 0

    async def set_evaluation_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """TODO"""

    async def get_script_path(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return ""

    async def set_script_path(self, algorithm_configuration_id: str, path: str) -> None:
        """TODO"""

    async def get_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None) -> str:
        """TODO"""
        return ""

    async def set_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None,
                                  parameter_value: GLib.Variant) -> None:
        """TODO"""
