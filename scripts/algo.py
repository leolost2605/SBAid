from gi.repository import Gio, GObject, GLib
from typing_extensions import override

from sbaid.model.algorithm.algorithm import Algorithm
from sbaid.model.algorithm.parameter_template import ParameterTemplate
from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.network_state import NetworkState


class AlgorithmImpl(Algorithm):
    def get_global_parameter_template(self) -> Gio.ListModel:
        store = Gio.ListStore.new(ParameterTemplate)
        store.append(ParameterTemplate("my param", GLib.VariantType.new("s"), None))
        store.append(ParameterTemplate("my other param", GLib.VariantType.new("d"), None))
        return store

    def get_cross_section_parameter_template(self) -> Gio.ListModel:
        store = Gio.ListStore.new(ParameterTemplate)
        store.append(ParameterTemplate("My cs Param", GLib.VariantType.new("s"), None))
        store.append(ParameterTemplate("My other cs Param", GLib.VariantType.new("d"), None))
        return Gio.ListStore.new(ParameterTemplate)

    def init(self, parameter_configuration_state: ParameterConfigurationState,
             network_state: NetworkState) -> None:
        pass

    def calculate_display(self, algorithm_input: Input) -> Display:
        return Display()  # Everything is OFF :)
