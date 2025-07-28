"""
The module containing the VissimNetwork class which represents the network
loaded from a file into vissim as a directed graph with links as vertices.
"""

from typing import Any
from sortedcontainers import SortedDict

from sbaid.common.location import Location


class InvalidPositionException(Exception):
    """Thrown if the given position wasn't found in the network"""


class InvalidSuccessorsException(Exception):
    """Thrown if the left most lane has no successor even though the link itself has successors"""


class _Link:
    __links_by_no: dict[int, '_Link']
    __no: int
    __successor_nos: list[int]
    __vissim_link: Any
    __points: list[Location]
    __cross_sections: SortedDict[float, str]

    @property
    def no(self) -> int:
        """Returns the unique number of this link, set by the vissim link."""
        return self.__no

    @property
    def successors(self) -> list['_Link']:
        """Returns a list of Links that follow this Link."""
        return list(map(lambda x: self.__links_by_no[x], self.__successor_nos))

    @property
    def left_most_successor(self) -> '_Link | None':
        """Returns the left most link that connects to this link."""
        successors = self.successors
        if not successors:
            return None

        if len(successors) == 1:
            return successors[0]

        # If we have more than one successor the successors are connectors, and we are not
        leftmost_lane = self.vissim_link.AttValue("NumLanes")
        for connector in self.successors:
            for lane in connector.vissim_link.Lanes.GetAll():
                for from_lane in lane.FromLanes.GetAll():
                    if from_lane.AttValue("Index") == leftmost_lane:  # Both are 1 indexed
                        return connector

        raise InvalidSuccessorsException("Leftmost lane has no successor")

    @property
    def points(self) -> list[Location]:
        """Returns points that make this link."""
        return self.__points.copy()

    @property
    def cross_sections(self) -> list[str]:
        """Returns the ids of the cross sections on this link."""
        return list(self.__cross_sections.values())

    @property
    def vissim_link(self) -> Any:
        """Returns the COM vissim link represented by this."""
        return self.__vissim_link

    def __init__(self, links_by_no: dict[int, '_Link'], vissim_link: Any,
                 connectors_by_from_link: dict[int, list[int]]) -> None:
        self.__links_by_no = links_by_no
        self.__no = vissim_link.AttValue("No")
        self.__successor_nos = []
        self.__vissim_link = vissim_link
        self.__points = []
        self.__cross_sections = SortedDict()

        if vissim_link.AttValue("IsConn"):
            self.__successor_nos.append(vissim_link.ToLink.AttValue("No"))
        elif self.__no in connectors_by_from_link:
            for connector_no in connectors_by_from_link[self.__no]:
                self.__successor_nos.append(connector_no)

        for point in vissim_link.LinkPolyPts.GetAll():
            self.__points.append(Location(point.AttValue("LatWGS84"), point.AttValue("LongWGS84")))

    def add_cross_section(self, pos: float, cross_section_id: str) -> None:
        """Adds the cross section with the given position to this link."""
        assert pos not in self.__cross_sections

        self.__cross_sections[pos] = cross_section_id

    def remove_cross_section(self, pos: float) -> None:
        """Removes the cross section with the given position from this link."""
        self.__cross_sections.pop(pos)

    def get_cross_section_successors(self, pos: float) -> list[str]:
        """
        Returns a list of the ids of cross sections that directly follow the cross section
        with the given position on any path.
        """
        assert pos in self.__cross_sections
        return self.__get_cs_successors(pos, set())

    def __get_cs_successors(self, pos: float, walked: set['_Link']) -> list[str]:
        if self in walked:
            return []

        walked.add(self)

        for p, cs_id in self.__cross_sections.items():
            if pos < p:
                return [cs_id]

        result = []
        for successor in self.successors:
            result += successor.__get_cs_successors(-1, walked)  # pylint: disable=protected-access

        return result

    def get_cross_section_links(self, pos: float) -> list[int]:
        """
        Returns all links the cross section at the given positon affects. That are all links
        that are following this link on any path where no other cross section is.
        """
        assert pos in self.__cross_sections
        return self.__get_cross_section_links(pos, set())

    def __get_cross_section_links(self, pos: float, walked: set['_Link']) -> list[Any]:
        if self in walked:
            return []

        walked.add(self)

        # We aren't the first link and we have other cross sections so we aren't
        # affected anymore
        if pos == -1 and self.__cross_sections:
            return []

        # We are the first link and we have another cross section that comes further down
        # on the link so only affect us (this is suboptimal anyways if this happens)
        if pos != -1 and list(self.__cross_sections.keys())[-1] != pos:
            return [self.vissim_link]

        if len(self.successors) != 1:
            return [self.vissim_link]

        # pylint: disable=protected-access
        return [self.vissim_link] + self.successors[0].__get_cross_section_links(-1, walked)

    def contains_point(self, point: Location) -> tuple[bool, float]:
        """
        Returns true and the distance from the start point of this link if the given point
        is on this link. Returns false and -1 otherwise.
        """
        other_point = self.__points[0]
        distance = 0.0
        for current_point in self.__points:
            if point.is_between(other_point, current_point):
                return True, distance + other_point.distance(point)

            distance += other_point.distance(current_point)
            other_point = current_point

        return False, -1


class VissimNetwork:
    """
    The vissim network as a directed graph of links. Links are the vertices.
    Contains methods that allow to query network information for cross section or links.
    """
    __links_by_no: dict[int, _Link]

    def __init__(self, vissim_network: Any):
        self.__links_by_no = {}

        connectors_by_from_link: dict[int, list[int]] = {}
        for connector in vissim_network.Links.GetFilteredSet("[IsConn]=1"):
            connector_no = connector.AttValue("No")
            connector_from_link_no = connector.FromLink.AttValue("No")

            if connector_from_link_no not in connectors_by_from_link:
                connectors_by_from_link[connector_from_link_no] = []

            connectors_by_from_link[connector_from_link_no].append(connector_no)

        for vissim_link in vissim_network.Links.GetAll():
            link = _Link(self.__links_by_no, vissim_link, connectors_by_from_link)
            self.__links_by_no[link.no] = link

    def add_cross_section(self, link_no: int, pos: float, cross_section_id: str) -> None:
        """
        Adds the cross section with the given id at the given link and position
        from the network.
        """
        self.__links_by_no[link_no].add_cross_section(pos, cross_section_id)

    def remove_cross_section(self, link_no: int, pos: float) -> None:
        """Removes the cross section at the given link and position from the network."""
        self.__links_by_no[link_no].remove_cross_section(pos)

    def get_cross_section_successors(self, link_no: int, pos: float) -> list[str]:
        """
        Returns the ids of the cross sections that are directly following the given cross
        section on any possible path.
        """
        return self.__links_by_no[link_no].get_cross_section_successors(pos)

    def get_cross_section_links(self, link_no: int, pos: float) -> list[Any]:
        """
        Returns the links that this cross section affects. Only useful for
        display or combined cross sections.
        """
        return self.__links_by_no[link_no].get_cross_section_links(pos)

    def get_link_and_position(self, location: Location) -> tuple[Any, float]:
        """
        Returns the link and the position on the link of the given location.
        Raises an InvalidPositionExcption if no valid link was found.
        """
        for link in self.__links_by_no.values():
            result, distance = link.contains_point(location)
            if result:
                return link.vissim_link, distance

        raise InvalidPositionException("No link with the given position found")

    def get_main_route(self, starting_link_no:
                       int | None = None) -> tuple[list[Location], list[str]]:
        """
        Returns the main route and the ids of the cross sections that are on it in the
        correct order.
        """
        link = None
        if starting_link_no is not None:
            link = self.__links_by_no[starting_link_no]
        else:
            link = next(iter(self.__links_by_no.values()))

        walked = set()
        points = link.points
        cross_sections = link.cross_sections
        while link := link.left_most_successor:
            if link in walked:
                break

            walked.add(link)

            points += link.points
            cross_sections += link.cross_sections

        return points, cross_sections
