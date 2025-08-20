import unittest
from unittest.mock import Mock, AsyncMock

from gi.repository import Gio, GLib

from sbaid.common.tag import Tag
from sbaid.model.algorithm.parameter_template import ParameterTemplate
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.algorithm_configuration.parameter import Parameter


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.__db_mock = Mock()
        self.__db_mock.get_parameter_value = AsyncMock()
        self.__db_mock.get_all_tag_ids_for_parameter = AsyncMock()
        self.__ac_id = "acid"
        self.__algo_mock = Mock()
        self.__tags = Gio.ListStore.new(Tag)
        self.__tags.append(Tag("id1", "My Tag"))
        self.__tags.append(Tag("id2", "My Tag 2"))

        global_store = Gio.ListStore.new(ParameterTemplate)
        global_store.append(ParameterTemplate("my global param", GLib.VariantType.new("s"), None))
        self.__algo_mock.get_global_parameter_template = Mock(return_value=global_store)

        cs_store = Gio.ListStore.new(ParameterTemplate)
        cs_store.append(ParameterTemplate("name", GLib.VariantType.new("s"), None))
        self.__algo_mock.get_cross_section_parameter_template = Mock(return_value=cs_store)

    async def test_parameter_configuration(self):
        simulator = DummySimulator()
        network = Network(simulator, self.__db_mock)
        parameter_config = ParameterConfiguration(network, self.__db_mock, self.__ac_id,
                                                  Gio.ListStore.new(Tag))
        parameter_config.set_algorithm(self.__algo_mock)
        await parameter_config.load()

        self.assertEqual(parameter_config.parameters.get_n_items (),
                         1 + network.cross_sections.get_n_items())

    async def test_parameter_export(self):
        param_1 = Parameter("param-1", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("value-1"), None,
                              self.__db_mock, self.__ac_id, self.__tags)
        param_2 = Parameter("param-2", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("value-2"), None,
                              self.__db_mock, self.__ac_id, self.__tags)
        param_3 = Parameter("param-3", GLib.VariantType.new("s"),
                  GLib.Variant.new_string("value-3"), None,
                  self.__db_mock, self.__ac_id, self.__tags)
        param_4 = Parameter("param-4", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("value-4"), None,
                              self.__db_mock, self.__ac_id, self.__tags)

        params = [param_1, param_2, param_3, param_4]
        simulator = DummySimulator()
        network = Network(simulator, self.__db_mock)
        parameter_config = ParameterConfiguration(network, self.__db_mock, self.__ac_id,
                                                  Gio.ListStore.new(Tag))

        parameter_config.export_to_csv()




if __name__ == '__main__':
    unittest.main()
