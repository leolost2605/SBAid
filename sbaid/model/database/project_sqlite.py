"""TODO"""
from gi.repository import GLib, Gio

from sbaid.model.database.project_database import ProjectDatabase


class ProjectSQLite(ProjectDatabase):
    """TODO"""

    async def open(self, file: Gio.File) -> None:
        """TODO"""

    async def get_created_at(self) -> GLib.DateTime:
        """TODO"""
        return GLib.DateTime.new_from_iso8601("0000-01-01T00:00:00")  # pylint: disable=no-member

    async def get_last_modified(self) -> GLib.DateTime:
        """TODO"""
        return GLib.DateTime.new_from_iso8601("0000-01-01T00:00:00")  # pylint: disable=no-member

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

    async def set_cross_section_name(self, cross_section_id: str, name: str) -> None:
        """TODO"""

    async def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str:
        """TODO"""
        return ""

    async def set_algorithm_configuration_name(self, algorithm_configuration_id: str, name: str)\
            -> None:
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

    async def set_evaluation_interval(self, algorithm_configuration_id: str, interval: int)\
            -> None:
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

    async def set_parameter_value(self, parameter_id: str, parameter_value: GLib.Variant) -> None:
        """TODO"""

    async def add_parameter(self, parameter_id: str, name: str, algorithm_configuration_id: str,
                            cross_section_id: str, value: GLib.Variant) -> None:
        """TODO"""

    async def remove_parameter(self, parameter_id: str) -> None:
        """TODO"""

    async def add_tag(self, tag_id: str, name: str) -> None:
        """TODO"""

    async def remove_tag(self, tag_id: str) -> None:
        """TODO"""

    async def add_parameter_tag(self, parameter_tag_id: str, parameter_id: str, tag_id: str)\
            -> None:
        """TODO"""

    async def remove_parameter_tag(self, parameter_tag_id: str) -> None:
        """TODO"""
