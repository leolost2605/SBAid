from typing import Any

from sbaid.common.coordinate import Coordinate


class InvalidPositionException(Exception):
    pass


class Link:
    __vissim_link: Any
    __points: list[Coordinate]

    def __init__(self, vissim_link: Any):
        self.__vissim_link = vissim_link
        self.__points = []

        for point in vissim_link.LinkPolyPts.GetAll():
            self.__points.append(Coordinate(point.AttValue("LatWGS84"), point.AttValue("LongWGS84")))

    @property
    def id(self) -> int:
        return self.__vissim_link.AttValue("No")

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
    __vissim_network: Any
    __links: list[Link]

    def __init__(self, network: Any):
        self.__vissim_network = network

        self.__links = []
        links = self.__vissim_network.Links.GetAll()
        for link in links:
            self.__links.append(Link(link))

    def get_link_and_position(self, location: Coordinate) -> tuple[Any, float]:
        for link in self.__links:
            result, distance = link.contains_point(location)
            if result:
                return link, distance

        raise InvalidPositionException("No link with the given position found")
