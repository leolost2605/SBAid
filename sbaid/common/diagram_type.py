"""This module defines the DiagramType class"""
class DiagramType:
    """This class represents a type of diagram.
    Attributes:
        diagram_type_id (str): The unique identifier for the diagram type.
        name (str): The name of the diagram type.
    """
    def __init__(self, diagram_type_id: str, name: str) -> None:
        self.diagram_type_id = diagram_type_id
        self.name = name
