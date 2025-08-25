import unittest
import unittest.mock as mock

from gi.repository import GLib, Gio

from sbaid.common.tag import Tag
from sbaid.view_model.algorithm_configuration.global_parameter import GlobalParameter


class GlobalParameterTestCase(unittest.TestCase):
    def test_global_parameter(self):
        model_param = mock.Mock()
        model_param.name = "My Name"
        model_param.value_type = GLib.VariantType.new("s")
        model_param.value = GLib.Variant.new_string("My Value")

        selected_tags = Gio.ListStore.new(Tag)
        selected_tags.append(Tag("my id", "Test"))

        model_param.selected_tags = selected_tags

        available_tags = Gio.ListStore.new(Tag)
        available_tags.append(Tag("my id", "Test"))
        available_tags.append(Tag("my other id", "Test Two"))

        param = GlobalParameter(model_param, available_tags)

        self.assertEqual(param.name, "My Name")
        self.assertEqual(param.value_type.dup_string(), "s")
        self.assertEqual(param.value.get_string(), "My Value")
        self.assertEqual(param.selected_tags.get_n_items(), 2)
        self.assertEqual(param.selected_tags.get_selection().get_size(), 1)
        self.assertEqual(param.selected_tags.is_selected(0), True)

        with self.assertRaises(TypeError):
            param.name = "My new name that shouldn't get set"

        param.update_value(GLib.Variant.new_string("My new value"))

        with self.assertRaises(ValueError):
            param.update_value(GLib.Variant.new_boolean(False))

        self.assertEqual(param.name, "My Name")
        self.assertEqual(param.value.get_string(), "My new value")

if __name__ == '__main__':
    unittest.main()
