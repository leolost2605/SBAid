import unittest
from typing import List

from gi.repository.GLib import Variant

from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation.parameter_state import ParameterState


class ParameterConfigurationTest(unittest.TestCase):

    def test_empty_parameter_configuration(self):
        parameter_configuration_state = ParameterConfigurationState([])
        self.assertEqual(parameter_configuration_state.parameter_states.get_n_items(), 0)
        self.assertEqual(parameter_configuration_state.parameter_states.get_n_items(), 0)

    def test_single_parameter_configuration_state(self):
        parameter_configuration_state = ParameterConfigurationState(
            [ParameterState("my_state",Variant.new_boolean(True), "my_cross_section")])
        self.assertEqual(parameter_configuration_state.parameter_states.get_n_items(), 1)
        self.assertEqual(parameter_configuration_state.parameter_states.get_item(0).name, "my_state")

    def test_cross_section_states(self):
        parameter_configuration_state = ParameterConfigurationState(
            [ParameterState("my_state", Variant.new_boolean(True), "my_cross_section"),
             ParameterState("my_state2", Variant.new_int64(69420), "my_cross_section2"),
             ParameterState("my_state3", Variant.new_double(99.99), "my_cross_section3")])
        self.assertEqual(parameter_configuration_state.parameter_states.get_n_items(), 3)
        self.assertEqual(parameter_configuration_state.parameter_states.get_item(0).name,
                         "my_state")
        self.assertEqual(parameter_configuration_state.parameter_states.get_item(1).value,
                         Variant.new_int64(69420))
        self.assertEqual(parameter_configuration_state.parameter_states.get_item(1).cross_section_id,
                         "my_cross_section2")
        self.assertEqual(parameter_configuration_state.parameter_states.get_item(2).value,
                         Variant.new_double(99.99))
