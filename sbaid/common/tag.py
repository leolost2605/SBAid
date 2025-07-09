"""This module defines the Tag class"""


class Tag:
    """This class represents a tag.
    Attributes:
        tag_id (str): The unique identifier for the tag.
        name (str): The name of the tag."""

    def __init__(self, tag_id: str, name: str) -> None:
        """Initialize the tag with an id and a name."""
        self.tag_id = tag_id
        self.name = name
