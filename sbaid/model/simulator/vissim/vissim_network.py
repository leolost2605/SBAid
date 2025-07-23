from typing import Any

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

    @property
    def no(self) -> int:
        return self.__no

    @property
    def successor_nos(self) -> list[int]:
        return self.__successor_nos.copy()

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
    def vissim_link(self) -> Any:
        return self.__vissim_link

    def __init__(self, links_by_no: dict[int, '_Link'], vissim_net: Any, vissim_link: Any):
        self.__links_by_no = links_by_no
        self.__no = vissim_link.AttValue("No")
        self.__vissim_link = vissim_link
        self.__points = []

        for point in vissim_link.LinkPolyPts.GetAll():
            self.__points.append(Coordinate(point.AttValue("LatWGS84"), point.AttValue("LongWGS84")))

        self.__successor_nos = []
        if vissim_link.AttValue("IsConn"):
            self.__successor_nos.append(vissim_link.ToLink.AttValue("No"))
        else:
            for connector in vissim_net.Links.GetFilteredSet("[IsConn]=1"):
                if connector.FromLink.AttValue("No") == self.no:
                    self.__successor_nos.append(connector.AttValue("No"))

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

        for vissim_link in vissim_network.Links.GetAll():
            link = _Link(self.__links_by_no, vissim_network, vissim_link)
            self.__links_by_no[link.no] = link

    def get_successors(self, link_no: int) -> list[int]:
        return self.__links_by_no[link_no].successor_nos

    def get_link_and_position(self, location: Coordinate) -> tuple[Any, float]:
        for link in self.__links_by_no.values():
            result, distance = link.contains_point(location)
            if result:
                return link.vissim_link, distance

        raise InvalidPositionException("No link with the given position found")

    def get_main_route(self, starting_link_no: int | None = None) -> list[Coordinate]:
        if starting_link_no is not None:
            link = self.__links_by_no[starting_link_no]
        else:
            link = next(iter(self.__links_by_no.values()))

        points = link.points
        while link := link.left_most_successor:
            points += link.points

        return points
