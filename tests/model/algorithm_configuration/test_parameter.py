import unittest
from gi.repository import GLib
from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.parameter import Parameter


class TestParameter(unittest.TestCase):
    test = GLib.VariantType.new("s")
    test_value = GLib.Variant.new_string("test_value")

    parameter = Parameter("parameter", test, test_value, None)

    def test_adding_tag(self):
        a = Tag (GLib.uuid_string_random(), "first_tag")
        b = Tag (GLib.uuid_string_random(), "second_tag")

        self.parameter.add_tag(a)
        self.parameter.add_tag(b)

        self.assertEqual(len(self.parameter.selected_tags), 2)

