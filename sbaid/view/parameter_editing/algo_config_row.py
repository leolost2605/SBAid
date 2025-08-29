"""
This module contains the AlgoConfigRow class displaying an algo config.
"""

import sys

import gi

from sbaid.view_model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.common.i18n import i18n
try:
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
    from gi.repository import Adw, Gtk, GObject, Gio, GLib, Gdk
except (ImportError, ValueError) as exc:
    print('Error: Dependencies not met.', exc)
    sys.exit(1)


class AlgoConfigRow(Adw.Bin):
    """
    This class displays an algo config.
    """
    __label: Gtk.Label
    __menu_model: Gio.Menu
    __menu: Gtk.PopoverMenu
    __label_binding: GObject.Binding | None = None

    def __init__(self) -> None:
        super().__init__()

        self.__menu_model = Gio.Menu()

        self.__menu = Gtk.PopoverMenu.new_from_model(self.__menu_model)
        self.__menu.set_has_arrow(False)
        self.__menu.set_halign(Gtk.Align.START)

        self.__label = Gtk.Label(xalign=0)

        gesture_click = Gtk.GestureClick(button=0, exclusive=True)
        gesture_click.connect("pressed", self.__on_clicked)

        self.set_child(self.__label)
        self.add_controller(gesture_click)

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

            if not self.__menu.get_parent():
                self.__menu.set_parent(self)

            self.__menu.set_pointing_to(rect)
            self.__menu.popup()
        else:
            self.activate_action("navigation.push", GLib.Variant.new_string("algo_config_view"))

    def bind(self, config: AlgorithmConfiguration) -> None:
        """
        Binds the given algo config to this row. Replaces any other algo config that may
        have been previously bound.
        :param config: the config to bind
        """
        if self.__label_binding:
            self.__label_binding.unbind()

        self.__label_binding = config.bind_property("name", self.__label, "label",
                                                    GObject.BindingFlags.SYNC_CREATE)

        self.__menu_model.remove_all()
        self.__menu_model.append(i18n._("Delete"), Gio.Action.print_detailed_name(
            "algo-config.delete", GLib.Variant.new_string(config.id)))
