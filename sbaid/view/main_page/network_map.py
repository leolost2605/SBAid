import sys

import gi

from sbaid import common
from sbaid.view_model.network.network import Network

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, GLib, Gio, Gtk, GObject, Shumate
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class NetworkMap(Adw.Bin):
    __network: Network
    __map: Shumate.SimpleMap
    __path_layer: Shumate.PathLayer
    __cross_sections_layer: Shumate.MarkerLayer

    def __init__(self,  network: Network) -> None:
        super().__init__()
        self.__network = network
        network.route_points.connect("items-changed", self.__on_route_changed)
        network.cross_sections.connect("items-changed", self.__on_cross_sections_changed)

        self.__map = Shumate.SimpleMap()
        self.__map.set_map_source(Shumate.RasterRenderer.new_from_url(r"https://tile.openstreetmap.org/{z}/{x}/{y}.png"))

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
            marker = Shumate.Marker.new()
            marker.set_location(loc.y, loc.x)
            self.__cross_sections_layer.add_marker(marker)
