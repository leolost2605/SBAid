import unittest
from unittest.mock import Mock

from gi.repository import Gio, GLib

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.parameter import Parameter as ModelParameter
from sbaid.model.simulator.dummy.dummy_cross_section import DummyCrossSection
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection
from sbaid.view_model.algorithm_configuration.cross_section_parameter import CrossSectionParameter
from sbaid.view_model.algorithm_configuration.global_parameter import GlobalParameter
from sbaid.view_model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.view_model.network.cross_section import CrossSection


class ParameterConfigurationTestCase(unittest.TestCase):
    def test_parameter_configuration(self):
        db_mock = Mock()

        global_param = ModelParameter("glp", GLib.VariantType.new("s"),
                                     GLib.Variant.new_string("My Value"), None)

        sim_cs_one = DummyCrossSection("id1", "name", CrossSectionType.COMBINED,
                                   Location(0,0), 5, True)

        sim_cs_two = DummyCrossSection("id2", "name", CrossSectionType.COMBINED,
                                   Location(0,0), 5, True)

        model_cross_section_one = ModelCrossSection(sim_cs_one, db_mock)
        model_cross_section_two = ModelCrossSection(sim_cs_two, db_mock)

        model_param = ModelParameter("My Name", GLib.VariantType.new("s"),
                                     GLib.Variant.new_string("My Value"), model_cross_section_one)

        other_param = ModelParameter("My Name", GLib.VariantType.new("s"),
                                     GLib.Variant.new_string("My Other Value"), model_cross_section_two)

        model_config = Mock()
        model_config.parameters = Gio.ListStore.new(ModelParameter)
        model_config.parameters.append(global_param)
        model_config.parameters.append(model_param)
        model_config.parameters.append(other_param)

        network_mock = Mock()
        network_mock.cross_sections = Gio.ListStore.new(CrossSection)

        tags = Gio.ListStore.new(Tag)

        config = ParameterConfiguration(model_config, network_mock, tags)

        self.assertEqual(config.parameters.get_n_items(), 2)
        self.assertIsInstance(config.parameters.get_item(0), GlobalParameter)
        self.assertIsInstance(config.parameters.get_item(1), CrossSectionParameter)


if __name__ == '__main__':
    unittest.main()
