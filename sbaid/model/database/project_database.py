"""This module contains the ProjectDatabase interface."""
from abc import ABC, abstractmethod

from gi.repository import GLib


class ProjectDatabase(ABC):
    """This interface contains methods that encapsulate necessary database behaviour."""

    @abstractmethod
    async def open(self) -> None:
        """Opens the file for the database."""

    @abstractmethod
    async def get_created_at(self) -> GLib.DateTime | None:
        """Return the GLib.DateTime when the project was created."""

    @abstractmethod
    async def set_last_opened(self, new_last_opened: GLib.DateTime) -> None:
        """Update the GLib.DateTime when the project was last opened."""

    @abstractmethod
    async def get_project_name(self) -> str | None:
        """Return the name of the project."""

    @abstractmethod
    async def set_project_name(self, name: str) -> None:
        """Update the name of the project."""

    @abstractmethod
    async def get_cross_section_name(self, cross_section_id: str) -> str | None:
        """Return the name of the cross_section with the given id."""

    @abstractmethod
    async def set_cross_section_name(self, cross_section_id: str, name: str) -> None:
        """Update the name of the cross_section with the given id."""

    @abstractmethod
    async def get_cross_section_hard_shoulder_active(self, cross_section_id: str) -> bool | None:
        """Return whether the hard should is active for the given cross section."""

    @abstractmethod
    async def set_cross_section_hard_shoulder_active(self, cross_section_id: str,
                                                     status: bool) -> None:
        """Update whether the hard should is active for the given cross section."""

    @abstractmethod
    async def get_cross_section_b_display_active(self, cross_section_id: str) -> bool | None:
        """Return whether the b is active for the given cross section."""

    @abstractmethod
    async def set_cross_section_b_display_active(self, cross_section_id: str, value: bool) -> None:
        """Update whether the b is active for the given cross section."""

    @abstractmethod
    async def get_algorithm_configuration_name(self, algorithm_configuration_id: str) -> str | None:
        """Return the name of the algorithm_configuration with the given id."""

    @abstractmethod
    async def set_algorithm_configuration_name(self, algorithm_configuration_id: str,
                                               name: str) -> None:
        """Update the name of the algorithm_configuration with the given id."""

    @abstractmethod
    async def get_last_opened(self) -> GLib.DateTime | None:
        """Return the GLib.DateTime when the project was last opened."""

    @abstractmethod
    async def get_algorithm_configuration(self, algorithm_configuration_id: str) \
            -> tuple[str, str, int, int, str, bool]:
        """Return the algorithm_configuration with the given id."""

    @abstractmethod
    async def get_all_algorithm_configuration_ids(self) -> list[str]:
        """Return all algorithm_configuration ids."""

    @abstractmethod
    async def get_selected_algorithm_configuration_id(self) -> str | None:
        """Return the currently selected algorithm_configuration id."""

    @abstractmethod
    async def set_selected_algorithm_configuration_id(self, configuration_id: str) -> None:
        """Update the currently selected algorithm_configuration id."""

    @abstractmethod
    async def get_display_interval(self, algorithm_configuration_id: str) -> int | None:
        """Return the display interval of the given algorithm_configuration id."""

    @abstractmethod
    async def set_display_interval(self, algorithm_configuration_id: str, interval: int) -> None:
        """Update the display interval of the given algorithm_configuration id."""

    @abstractmethod
    async def get_evaluation_interval(self, algorithm_configuration_id: str) -> int | None:
        """Return the evaluation interval of the given algorithm_configuration id."""

    @abstractmethod
    async def set_evaluation_interval(self, algorithm_configuration_id: str,
                                      interval: int) -> None:
        """Update the evaluation interval of the given algorithm_configuration id."""

    @abstractmethod
    async def get_script_path(self, algorithm_configuration_id: str) -> str | None:
        """Return the scrip path of the given algorithm_configuration id."""

    @abstractmethod
    async def set_script_path(self, algorithm_configuration_id: str, path: str) -> None:
        """Update the script path of the given algorithm_configuration id."""

    @abstractmethod
    async def get_all_parameters(self, algorithm_configuration_id: str) -> list[tuple[str, str]]:
        """Return all parameters of the given algorithm_configuration id."""

    @abstractmethod
    async def get_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None) -> GLib.Variant | None:
        """Return the value of the parameter of the given algorithm configuration
        and parameter and possibly cross section."""

    @abstractmethod
    async def set_parameter_value(self, algorithm_configuration_id: str, parameter_name: str,
                                  cross_section_id: str | None,
                                  parameter_value: GLib.Variant) -> None:
        """Update the value of the parameter of the given algorithm configuration,
        parameter name and cross section."""

    @abstractmethod
    async def add_cross_section(self, cross_section_id: str) -> None:
        """Add a new cross section with an id."""

    @abstractmethod
    async def remove_cross_section(self, cross_section_id: str) -> None:
        """Remove a cross section from the database."""

    @abstractmethod
    async def add_parameter(self, algorithm_configuration_id: str, name: str,
                            cross_section_id: str | None) -> None:
        """Add a new parameter from the given algorithm configuration and parameter."""

    @abstractmethod
    async def remove_parameter(self, algorithm_configuration_id: str, name: str,
                               cross_section_id: str | None) -> None:
        """Remove a parameter with the given algorithm configuration and parameter name
        and possibly cross section."""

    @abstractmethod
    async def add_algorithm_configuration(self, algorithm_configuration_id: str, name: str,
                                          evaluation_interval: int, display_interval: int,
                                          script_path: str, is_selected: bool = True) -> None:
        """Add a new algorithm configuration to the database."""

    @abstractmethod
    async def remove_algorithm_configuration(self, algorithm_configuration_id: str) -> None:
        """Remove a algorithm configuration from the database."""

    @abstractmethod
    async def add_tag(self, tag_id: str, name: str) -> None:
        """Add a new tag to the database."""

    @abstractmethod
    async def remove_tag(self, tag_id: str) -> None:
        """Remove a tag from the database."""

    @abstractmethod
    async def get_tag_name(self, tag_id: str) -> str | None:
        """Return the name of the given tag_id."""

    @abstractmethod
    async def add_parameter_tag(self, parameter_tag_id: str, parameter_name: str,
                                algorithm_configuration_id: str, cross_section_id: str | None,
                                tag_id: str) -> None:
        """Add a new parameter tag entry which represents a tag
        belonging to the given parameter."""

    @abstractmethod
    async def remove_parameter_tag(self, parameter_tag_id: str) -> None:
        """Remove a parameter tag entry."""

    @abstractmethod
    async def get_all_tags(self) -> list[tuple[str, str]]:
        """Return the id and name for all tags in this project."""

    @abstractmethod
    async def get_all_tag_ids_for_parameter(self, algorithm_configuration_id: str,
                                            parameter_name: str,
                                            cross_section_id: str | None) -> list[str]:
        """Return all tag ids belonging to the given parameter."""
