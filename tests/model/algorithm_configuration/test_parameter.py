import unittest
import unittest.mock as mock

from gi.repository import GLib

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.parameter import Parameter, TagAlreadySetException, \
    TagNotFoundException


class ParameterTestCase(unittest.TestCase):
    def test_properties(self):
        parameter = Parameter("My Param", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("my value"), None)
        self.assertEqual(parameter.value.get_string(), "my value")
        self.assertEqual(parameter.name, "My Param")
        self.assertEqual(parameter.cross_section, None)

        parameter.value = GLib.Variant.new_string("a new value")

        self.assertEqual(parameter.value.get_string(), "a new value")

        parameter.value = GLib.Variant.new_boolean(True) # this should fail

        self.assertEqual(parameter.value.get_string(), "a new value")

    def test_initialize(self):
        parameter_no_default = Parameter("My param", GLib.VariantType.new("b"),
                              None, None)

        self.assertEqual(parameter_no_default.value, None)

        param_wrong_default = Parameter("My param", GLib.VariantType.new("b"),
                              GLib.Variant.new_string("my value of the wrong type"), None)

        self.assertEqual(param_wrong_default.value, None)

    def test_tags(self):
        parameter = Parameter("My Param", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("my value"), None)

        self.assertEqual(parameter.selected_tags.get_n_items(), 0)

        tag1 = Tag("id1", "My Tag")
        tag2 = Tag("id2", "My Tag 2")
        tag_not_added = Tag("id3", "My Tag that wasn't added")
        parameter.add_tag(tag1)
        parameter.add_tag(tag2)

        self.assertEqual(parameter.selected_tags.get_n_items(), 2)

        self.assertRaises(TagAlreadySetException, parameter.add_tag, tag1)

        parameter.remove_tag(tag1)

        self.assertEqual(parameter.selected_tags.get_n_items(), 1)

        self.assertRaises(TagNotFoundException, parameter.remove_tag, tag1)

        self.assertRaises(TagNotFoundException, parameter.remove_tag, tag_not_added)


if __name__ == '__main__':
    unittest.main()
