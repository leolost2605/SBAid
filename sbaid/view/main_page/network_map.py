"""
This module contains the network map.
"""

import sys
from typing import cast

import gi

from sbaid import common
from sbaid.view.main_page.cross_section_marker import CrossSectionMarker
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gio, Shumate
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionNotFoundError(Exception):
    """Raised when it was tried to go to a cross section that doesn't exist."""


class NetworkMap(Adw.Bin):
    """
    Displays the world map with the route and cross sections on it.
    """

    __project_id: str
    __network: Network
    __map: Shumate.SimpleMap
    __path_layer: Shumate.PathLayer
    __cross_sections_layer: Shumate.MarkerLayer

    __show_details_after_animation: CrossSectionMarker | None = None

    def __init__(self, project_id: str, network: Network) -> None:
        super().__init__()

        self.__project_id = project_id
        self.__network = network
        network.route_points.connect("items-changed", self.__on_route_changed)
        network.cross_sections.connect("items-changed", self.__on_cross_sections_changed)

        self.__map = Shumate.SimpleMap()
        self.__map.set_map_source(Shumate.RasterRenderer.new_from_url(
            r"https://tile.openstreetmap.org/{z}/{x}/{y}.png"))
        self.__map.get_map().connect("animation-completed", self.__on_animation_completed)

        self.__path_layer = Shumate.PathLayer.new(self.__map.get_viewport())
        self.__cross_sections_layer = Shumate.MarkerLayer.new(self.__map.get_viewport())

        self.__map.add_overlay_layer(self.__path_layer)
        self.__map.add_overlay_layer(self.__cross_sections_layer)

        self.set_child(self.__map)

        self.__on_route_changed(network.route_points, 0, 0,
                                network.route_points.get_n_items())

        self.__on_cross_sections_changed(network.cross_sections, 0, 0,
                                         network.cross_sections.get_n_items())

    def __on_route_changed(self, model: Gio.ListModel, pos: int, removed: int, added: int) -> None:
        self.__path_layer.remove_all()

        for location in common.list_model_iterator(self.__network.route_points):
            coord = Shumate.Coordinate(latitude=location.y, longitude=location.x)
            self.__path_layer.add_node(coord)

    def __on_cross_sections_changed(self, model: Gio.ListModel, pos: int,
                                    removed: int, added: int) -> None:
        self.__cross_sections_layer.remove_all()

        for cross_section in common.list_model_iterator(self.__network.cross_sections):
            loc = cross_section.location
            marker = Shumate.Marker()
            marker.set_child(CrossSectionMarker(self.__project_id, self.__network, cross_section))
            marker.set_location(loc.y, loc.x)
            self.__cross_sections_layer.add_marker(marker)

    def show_cross_section_details(self, cross_section: CrossSection) -> None:
        """
        Moves the map to the location of the cross section and shows a popup with details.
        :param cross_section: the cross section to show details for
        """
        self.__map.get_map().go_to_full(cross_section.location.y, cross_section.location.x, 10)

        for marker in self.__cross_sections_layer.get_markers():
            cs_marker = cast(CrossSectionMarker, marker.get_child())
            if cs_marker.cross_section == cross_section:
                self.__show_details_after_animation = cs_marker
                return

        raise CrossSectionNotFoundError

    def __on_animation_completed(self, shumate_map: Shumate.Map) -> None:
        if self.__show_details_after_animation is not None:
            self.__show_details_after_animation.show_details()
            self.__show_details_after_animation = None
