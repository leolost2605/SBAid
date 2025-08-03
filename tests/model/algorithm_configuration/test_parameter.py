import unittest
import unittest.mock as mock

from gi.repository import GLib, Gio

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.parameter import Parameter, TagAlreadySetException, \
    TagNotFoundException


class ParameterTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__db_mock = mock.Mock()
        self.__db_mock.add_parameter_tag = mock.AsyncMock()
        self.__db_mock.remove_parameter_tag = mock.AsyncMock()
        self.__db_mock.set_parameter_value = mock.AsyncMock()
        self.__ac_id = "acid"
        self.__tags = Gio.ListStore.new(Tag)
        self.__tags.append(Tag("id1", "My Tag"))
        self.__tags.append(Tag("id2", "My Tag 2"))

    async def test_properties(self):
        parameter = Parameter("My Param", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("my value"), None,
                              self.__db_mock, self.__ac_id, self.__tags)
        self.assertEqual(parameter.value.get_string(), "my value")
        self.assertEqual(parameter.name, "My Param")
        self.assertEqual(parameter.cross_section, None)

        parameter.value = GLib.Variant.new_string("a new value")

        self.assertEqual(parameter.value.get_string(), "a new value")

        parameter.value = GLib.Variant.new_boolean(True) # this should fail

        self.assertEqual(parameter.value.get_string(), "a new value")

    async def test_initialize(self):
        parameter_no_default = Parameter("My param", GLib.VariantType.new("b"),
                                   None, None, self.__db_mock, self.__ac_id,
                                         self.__tags)

        self.assertEqual(parameter_no_default.value, None)

        param_wrong_default = Parameter(
            "My param", GLib.VariantType.new("b"),
            GLib.Variant.new_string("my value of the wrong type"), None,
            self.__db_mock, self.__ac_id, self.__tags)

        self.assertEqual(param_wrong_default.value, None)

    async def test_tags(self):
        parameter = Parameter("My Param", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("my value"), None,
                              self.__db_mock, self.__ac_id, self.__tags)

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
        self.assertEqual(parameter.selected_tags.get_item(0).tag_id, "id2")

        self.__tags.remove(1)

        self.assertEqual(parameter.selected_tags.get_n_items(), 0)


if __name__ == '__main__':
    unittest.main()
