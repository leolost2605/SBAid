import unittest
from unittest.mock import Mock, AsyncMock
from gi.repository import GLib, Gio

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.csv_parameter_exporter import CSVParameterExporter
from sbaid.model.algorithm_configuration.exporter_factory import ExporterFactory
from sbaid.model.algorithm_configuration.parameter import Parameter
from sbaid.model.algorithm.parameter_template import ParameterTemplate
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.network.network import Network
from tests.mock_cross_section import MockCrossSection
from tests.model.algorithm_configuration.mock_parameter_configuration import MockParameterConfiguration


class ParameterExportTest(unittest.IsolatedAsyncioTestCase):

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

        simulator = DummySimulator()
        self.__network = Network(simulator, self.__db_mock)

    def test_find_exporter(self):
        factory = ExporterFactory()
        self.assertIsInstance(factory.get_exporter("csv"), CSVParameterExporter)

    async def test_parameter_export(self):
        sim_cs_1 = MockCrossSection("cs_id_1", "cs_1", CrossSectionType.COMBINED,
                                  Location(0,0), 4)
        cross_section_1 = CrossSection(sim_cs_1, self.__db_mock)

        sim_cs_2 = MockCrossSection("cs_id_2", "cs_2", CrossSectionType.COMBINED,
                                  Location(0, 0), 4)
        cross_section_2 = CrossSection(sim_cs_2, self.__db_mock)

        sim_cs_3 = MockCrossSection("cs_id_3", "cs_3", CrossSectionType.COMBINED,
                                    Location(0, 0), 4)
        cross_section_3 = CrossSection(sim_cs_3, self.__db_mock)

        sim_cs_4 = MockCrossSection("cs_id_4", "cs_4", CrossSectionType.COMBINED,
                                    Location(0,0), 4)
        cross_section_4 = CrossSection(sim_cs_4, self.__db_mock)


        param_1 = Parameter("param-1", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("str-value"), cross_section_1,
                              self.__db_mock, self.__ac_id, self.__tags)
        param_11 = Parameter("param-2", GLib.VariantType.new("b"),
                            GLib.Variant.new_string("True"), cross_section_1,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_12 = Parameter("param-3", GLib.VariantType.new("s"),
                            GLib.Variant.new_string("str-value"), cross_section_1,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_13 = Parameter("param-4", GLib.VariantType.new("d"),
                            GLib.Variant.new_double(2.1), cross_section_1,
                            self.__db_mock, self.__ac_id, self.__tags)

        param_2 = Parameter("param-1", GLib.VariantType.new("s"),
                              GLib.Variant.new_string("str-value"), cross_section_2,
                              self.__db_mock, self.__ac_id, self.__tags)
        param_21 = Parameter("param-2", GLib.VariantType.new("b"),
                            GLib.Variant.new_boolean(True), cross_section_2,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_22 = Parameter("param-3", GLib.VariantType.new("s"),
                            GLib.Variant.new_string("str-value"), cross_section_2,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_23 = Parameter("param-4", GLib.VariantType.new("d"),
                            GLib.Variant.new_double(1.4), cross_section_2,
                            self.__db_mock, self.__ac_id, self.__tags)

        param_3 = Parameter("param-1", GLib.VariantType.new("s"),
                  GLib.Variant.new_string("value-3"), cross_section_3,
                  self.__db_mock, self.__ac_id, self.__tags)
        param_31 = Parameter("param-2", GLib.VariantType.new("b"),
                            GLib.Variant.new_boolean(True), cross_section_3,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_32 = Parameter("param-3", GLib.VariantType.new("s"),
                            GLib.Variant.new_string("value-3"), cross_section_3,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_33 = Parameter("param-4", GLib.VariantType.new("d"),
                            GLib.Variant.new_double(1.5), cross_section_3,
                            self.__db_mock, self.__ac_id, self.__tags)

        param_4 = Parameter("param-1", GLib.VariantType.new("s"),
                            GLib.Variant.new_string("value-3"), cross_section_4,
                            self.__db_mock, self.__ac_id, self.__tags)
        param_41 = Parameter("param-2", GLib.VariantType.new("b"),
                             GLib.Variant.new_boolean(False), cross_section_4,
                             self.__db_mock, self.__ac_id, self.__tags)
        param_42 = Parameter("param-3", GLib.VariantType.new("s"),
                             GLib.Variant.new_string("value-3"), cross_section_4,
                             self.__db_mock, self.__ac_id, self.__tags)
        param_43 = Parameter("param-4", GLib.VariantType.new("d"),
                             GLib.Variant.new_double(5.3), cross_section_4,
                             self.__db_mock, self.__ac_id, self.__tags)

        params = Gio.ListStore.new(Parameter)
        params.append(param_1)
        params.append(param_11)
        params.append(param_12)
        params.append(param_13)
        params.append(param_2)
        params.append(param_21)
        params.append(param_22)
        params.append(param_23)
        params.append(param_3)
        params.append(param_31)
        params.append(param_32)
        params.append(param_33)
        params.append(param_4)
        params.append(param_41)
        params.append(param_42)
        params.append(param_43)
        parameter_config = MockParameterConfiguration(params)

        await parameter_config.export_parameter_configuration("param-export.csv", "csv")

if __name__ == '__main__':
    unittest.main()
