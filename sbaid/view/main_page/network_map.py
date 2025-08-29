"""
This module contains the network map.
"""

import sys
from typing import cast

import gi

from sbaid import common
from sbaid.common.location import Location
from sbaid.view import utils
from sbaid.view.main_page.cross_section_icon import CrossSectionIcon
from sbaid.view.main_page.add_new_cross_section_dialog import AddNewCrossSectionDialog
from sbaid.view.main_page.cross_section_marker import CrossSectionMarker
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view_model.network.network import Network
from sbaid.common.i18n import i18n

try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    gi.require_version('Shumate', '1.0')
    from gi.repository import Adw, Gio, Shumate, Gdk, Gtk, GLib, GObject
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class CrossSectionNotFoundError(Exception):
    """Raised when it was tried to go to a cross section that doesn't exist."""


class NetworkMap(Adw.Bin):  # pylint: disable=too-many-instance-attributes
    """
    Displays the world map with the route and cross sections on it.
    """

    __project_id: str
    __network: Network
    __map: Shumate.SimpleMap
    __path_layer: Shumate.PathLayer
    __cross_sections_layer: Shumate.MarkerLayer

    __show_details_after_animation: CrossSectionMarker | None = None
    __moving_cross_section: CrossSection | None = None

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
        self.__path_layer.set_stroke_color(Gdk.RGBA(0.023529411764705882, 0.054901960784313725,
                                                    0.5019607843137255, 1.0))
        self.__path_layer.set_stroke_width(5)
        self.__cross_sections_layer = Shumate.MarkerLayer.new(self.__map.get_viewport())

        self.__map.add_overlay_layer(self.__path_layer)
        self.__map.add_overlay_layer(self.__cross_sections_layer)

        self.__move_icon = CrossSectionIcon()
        self.__move_icon.set_halign(Gtk.Align.CENTER)
        self.__move_icon.set_valign(Gtk.Align.CENTER)
        self.__move_icon.set_visible(False)

        self.__move_button = Gtk.Button.new_with_label(i18n._("Move"))
        self.__move_button.add_css_class("suggested-action")
        self.__move_button.set_visible(False)
        self.__move_button.connect("clicked", lambda button: self.__end_move(True))

        self.__cancel_move_button = Gtk.Button.new_with_label(i18n._("Cancel"))
        self.__cancel_move_button.add_css_class("osd")
        self.__cancel_move_button.set_visible(False)
        self.__cancel_move_button.connect("clicked", lambda button: self.__end_move(False))

        button_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 3)
        button_box.set_margin_bottom(6)
        button_box.set_margin_end(6)
        button_box.set_halign(Gtk.Align.END)
        button_box.set_valign(Gtk.Align.END)
        button_box.append(self.__cancel_move_button)
        button_box.append(self.__move_button)

        overlay = Gtk.Overlay(child=self.__map)
        overlay.add_overlay(self.__move_icon)
        overlay.add_overlay(button_box)

        self.__menu_model = Gio.Menu()

        self.__menu = Gtk.PopoverMenu.new_from_model(self.__menu_model)
        self.__menu.set_has_arrow(False)
        self.__menu.set_halign(Gtk.Align.START)

        gesture_click = Gtk.GestureClick(button=0, exclusive=True)
        gesture_click.connect("pressed", self.__on_clicked)

        self.set_child(overlay)
        self.add_controller(gesture_click)

        self.__on_route_changed(network.route_points, 0, 0,
                                network.route_points.get_n_items())

        self.__on_cross_sections_changed(network.cross_sections, 0, 0,
                                         network.cross_sections.get_n_items())

        self.install_action("cross-section.add", "(dd)", self.__on_add_cross_section)
        self.install_action("cross-section.move", "s", self.__on_move_cross_section)

    def __on_route_changed(self, model: Gio.ListModel, pos: int, removed: int, added: int) -> None:
        self.__path_layer.remove_all()

        for location in common.list_model_iterator(self.__network.route_points):
            coord = Shumate.Coordinate(latitude=location.y, longitude=location.x)
            self.__path_layer.add_node(coord)

    def __on_cross_sections_changed(self, model: Gio.ListModel, pos: int,
                                    removed: int, added: int) -> None:
        self.__cross_sections_layer.remove_all()

        for c in common.list_model_iterator(self.__network.cross_sections):
            cross_section = cast(CrossSection, c)
            marker = Shumate.Marker()
            marker.set_child(CrossSectionMarker(self.__project_id, self.__network, cross_section))
            cross_section.bind_property("location", marker, "latitude",
                                        GObject.BindingFlags.SYNC_CREATE,
                                        lambda binding, loc: loc.y)
            cross_section.bind_property("location", marker, "longitude",
                                        GObject.BindingFlags.SYNC_CREATE,
                                        lambda binding, loc: loc.x)
            self.__cross_sections_layer.add_marker(marker)

    def __get_marker_for_cross_section(self, cross_section: CrossSection) -> CrossSectionMarker:
        for marker in self.__cross_sections_layer.get_markers():
            cs_marker = cast(CrossSectionMarker, marker.get_child())
            if cs_marker.cross_section == cross_section:
                return cs_marker

        raise CrossSectionNotFoundError

    def show_cross_section_details(self, cross_section: CrossSection) -> None:
        """
        Moves the map to the location of the cross section and shows a popup with details.
        :param cross_section: the cross section to show details for
        """
        self.__show_details_after_animation = self.__get_marker_for_cross_section(cross_section)
        self.__map.get_map().go_to_full(cross_section.location.y, cross_section.location.x, 10)

    def __on_animation_completed(self, shumate_map: Shumate.Map) -> None:
        if self.__show_details_after_animation is not None:
            self.__show_details_after_animation.show_details()
            self.__show_details_after_animation = None

    def __on_clicked(self, click: Gtk.GestureClick, n_press: int, x: float, y: float) -> None:
        event = click.get_current_event()

        if not event:
            return

        if event.triggers_context_menu():
            click.set_state(Gtk.EventSequenceState.CLAIMED)
            click.reset()

            rect = Gdk.Rectangle()
            rect.x = int(x)
            rect.y = int(y)

            builder = GLib.VariantBuilder(GLib.VariantType("(dd)"))
            builder.add_value(GLib.Variant.new_double(x))
            builder.add_value(GLib.Variant.new_double(y))
            target = builder.end()

            self.__menu_model.remove_all()
            self.__menu_model.append(i18n._("Add new cross section"),
                                     Gio.Action.print_detailed_name(
                "cross-section.add", target))

            if not self.__menu.get_parent():
                self.__menu.set_parent(self)

            self.__menu.set_pointing_to(rect)
            self.__menu.popup()

    def __on_add_cross_section(self, widget: Gtk.Widget, action_name: str,
                               parameter: GLib.Variant | None) -> None:
        if parameter is None:
            return

        if not parameter.get_type_string() == "(dd)":
            return

        x = parameter.get_child_value(0).get_double()
        y = parameter.get_child_value(1).get_double()

        viewport = self.__map.get_viewport()

        lat, long = viewport.widget_coords_to_location(self.__map, x, y)

        AddNewCrossSectionDialog(self.__network, long, lat).present(cast(Gtk.Window,
                                                                         self.get_root()))

    def __on_move_cross_section(self, widget: Gtk.Widget, action_name: str,
                                parameter: GLib.Variant | None) -> None:
        if parameter is None:
            return

        cs_id = parameter.get_string()

        if cs_id is None:
            return

        for cs in self.__network.cross_sections:
            cross_section = cast(CrossSection, cs)
            if cross_section.id == cs_id:
                self.__start_move(cross_section)

    def __start_move(self, cross_section: CrossSection) -> None:
        if self.__moving_cross_section:
            self.__end_move(False)

        self.__moving_cross_section = cross_section

        marker = self.__get_marker_for_cross_section(cross_section)
        marker.set_visible(False)

        self.__move_icon.set_visible(True)
        self.__move_button.set_visible(True)
        self.__cancel_move_button.set_visible(True)

    def __end_move(self, commit: bool) -> None:
        if not self.__moving_cross_section:
            return

        self.__move_icon.set_visible(False)
        self.__move_button.set_visible(False)
        self.__cancel_move_button.set_visible(False)

        if commit:
            cs_id = self.__moving_cross_section.id

            viewport = self.__map.get_viewport()
            x = viewport.get_longitude()
            y = viewport.get_latitude()
            new_location = Location(x, y)

            utils.run_coro_with_error_reporting(
                self.__network.move_cross_section(cs_id, new_location))

        marker = self.__get_marker_for_cross_section(self.__moving_cross_section)
        marker.set_visible(True)

        self.__moving_cross_section = None
