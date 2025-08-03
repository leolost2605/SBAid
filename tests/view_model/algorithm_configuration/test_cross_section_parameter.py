import unittest
import unittest.mock as mock

import gi

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.model.simulator.dummy.dummy_cross_section import DummyCrossSection

gi.require_version('Gtk', '4.0')
from gi.repository import GLib, Gio, Gtk

from sbaid.common.tag import Tag
from sbaid.view_model.algorithm_configuration.cross_section_parameter import CrossSectionParameter
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.model.algorithm_configuration.parameter import Parameter as ModelParameter
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection


class CrossSectionParameterTestCase(unittest.TestCase):
    def test_cross_section_parameter(self):
        db_mock = mock.Mock()
        tags = Gio.ListStore.new(Tag)
        acid = "acid"

        sim_cs_one = DummyCrossSection("id1", "name", CrossSectionType.COMBINED,
                                   Location(0,0), 5, True)

        sim_cs_two = DummyCrossSection("id2", "name", CrossSectionType.COMBINED,
                                   Location(0,0), 5, True)

        model_cross_section_one = ModelCrossSection(sim_cs_one, db_mock)
        model_cross_section_two = ModelCrossSection(sim_cs_two, db_mock)

        model_param = ModelParameter("My Name", GLib.VariantType.new("s"),
                                     GLib.Variant.new_string("My Value"), model_cross_section_one,
                                     db_mock, acid, tags)

        other_param = ModelParameter("My Name", GLib.VariantType.new("s"),
                                     GLib.Variant.new_string("My Other Value"), model_cross_section_two,
                                     db_mock, acid, tags)

        params = Gio.ListStore.new(ModelParameter)
        params.append(model_param)
        params.append(other_param)

        cross_sections = Gio.ListStore.new(CrossSection)
        cross_sections.append(CrossSection(model_cross_section_one))
        cross_sections.append(CrossSection(model_cross_section_two))

        selected_cross_section = Gtk.MultiSelection.new(cross_sections)

        available_tags = Gio.ListStore()
        available_tags.append(Tag("my id", "Test"))
        available_tags.append(Tag("my other id", "Test Two"))

        param = CrossSectionParameter(params, selected_cross_section, available_tags)

        self.assertEqual(param.name, "My Name")
        self.assertEqual(param.value_type.dup_string(), "s")
        self.assertEqual(param.selected_tags.get_n_items(), 2)
        self.assertEqual(param.selected_tags.get_selection().get_size(), 0)

        with self.assertRaises(TypeError):
            param.name = "My new name that shouldn't get set"

        self.assertEqual(param.name, "My Name")

        self.assertEqual(param.inconsistent, False)
        self.assertEqual(param.value, None)

        selected_cross_section.select_item(1, False)

        self.assertEqual(param.inconsistent, False)
        self.assertEqual(param.value.get_string(), "My Other Value")

        selected_cross_section.select_item(0, False)

        self.assertEqual(param.inconsistent, True)
        self.assertEqual(param.value, None)

        param.value = GLib.Variant.new_string("My new value")
        param.value = GLib.Variant.new_boolean(False)  # Should get rejected

        self.assertEqual(param.value.get_string(), "My new value")
        self.assertEqual(param.inconsistent, False)

if __name__ == '__main__':
    unittest.main()
