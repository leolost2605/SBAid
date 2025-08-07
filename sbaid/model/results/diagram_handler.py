"""This module contains the DiagramHandler class."""

from abc import ABC, abstractmethod
from sbaid.common.diagram_type import DiagramType


class DiagramHandler(ABC):
    """Interface implemented by every diagram generator."""

    @abstractmethod
    def get_diagram_type(self) -> DiagramType:
        """Returns diagram type of the generator"""
