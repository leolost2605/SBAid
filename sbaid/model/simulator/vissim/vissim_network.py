from typing import Any
from sortedcontainers import SortedDict

from sbaid.common.coordinate import Coordinate


class InvalidPositionException(Exception):
    pass


class InvalidSuccessorsException(Exception):
    pass


class _Link:
    __links_by_no: dict[int, '_Link']
    __no: int
    __successor_nos: list[int]
    __vissim_link: Any
    __points: list[Coordinate]
    __cross_sections: SortedDict[float, str]

    @property
    def no(self) -> int:
        return self.__no

    @property
    def successors(self) -> list['_Link']:
        return list(map(lambda x: self.__links_by_no[x], self.__successor_nos))

    @property
    def left_most_successor(self) -> '_Link | None':
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
    def points(self) -> list[Coordinate]:
        return self.__points.copy()

    @property
    def cross_sections(self) -> list[str]:
        return list(self.__cross_sections.values())

    @property
    def vissim_link(self) -> Any:
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
            self.__points.append(Coordinate(point.AttValue("LatWGS84"), point.AttValue("LongWGS84")))

    def add_cross_section(self, pos: float, cross_section_id: str):
        assert pos not in self.__cross_sections

        self.__cross_sections[pos] = cross_section_id

    def remove_cross_section(self, pos: float):
        self.__cross_sections.pop(pos)

    def get_cross_section_successors(self, pos: float) -> list[str]:
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
            result += successor.__get_cs_successors(-1, walked)

        return result

    def get_cross_section_links(self, pos: float) -> list[int]:
        assert pos in self.__cross_sections
        return self.__get_cross_section_links(pos, set())

    def __get_cross_section_links(self, pos: float, walked: set['_Link']) -> list[Any]:
        if self in walked:
            return []

        walked.add(self)

        if pos == -1 and self.__cross_sections:
            return []

        if pos != -1 and list(self.__cross_sections.keys())[-1] != pos:
            return [self.vissim_link]

        if len(self.successors) != 1:
            return [self.vissim_link]

        return [self.vissim_link] + self.successors[0].__get_cross_section_links(-1, walked)

    def contains_point(self, point: Coordinate) -> tuple[bool, float]:
        other_point = self.__points[0]
        distance = 0
        for current_point in self.__points:
            if point.is_between(other_point, current_point):
                return True, distance + other_point.distance(point)

            distance += other_point.distance(current_point)
            other_point = current_point

        return False, -1


class VissimNetwork:
    __links_by_no: dict[int, _Link]
    __vissim_network: Any

    def __init__(self, vissim_network: Any):
        self.__links_by_no = {}
        self.__vissim_network = vissim_network

        connectors_by_from_link = {}
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
        self.__links_by_no[link_no].add_cross_section(pos, cross_section_id)

    def remove_cross_section(self, link_no: int, pos: float) -> None:
        self.__links_by_no[link_no].remove_cross_section(pos)

    def get_cross_section_successors(self, link_no: int, pos: float) -> list[str]:
        return self.__links_by_no[link_no].get_cross_section_successors(pos)

    def get_cross_section_links(self, link_no: int, pos: float) -> list[Any]:
        """
        Returns the links that this cross section affects. Only useful for
        display or combined cross sections.
        """
        return self.__links_by_no[link_no].get_cross_section_links(pos)

    def get_link_and_position(self, location: Coordinate) -> tuple[Any, float]:
        for link in self.__links_by_no.values():
            result, distance = link.contains_point(location)
            if result:
                return link.vissim_link, distance

        raise InvalidPositionException("No link with the given position found")

    def get_main_route(self, starting_link_no: int | None = None) -> tuple[list[Coordinate], list[str]]:
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
