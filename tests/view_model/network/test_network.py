import unittest
from unittest.mock import Mock, AsyncMock

from gi.repository import Gio

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.view_model.network.network import Network
from sbaid.model.network.cross_section import CrossSection as ModelCrossSection


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_network(self):
        sim_cross_section_mock = Mock()
        sim_cross_section_mock.id = "My id"
        sim_cross_section_mock.lanes = 5
        model_cross_section = ModelCrossSection(sim_cross_section_mock, Mock())

        create_cross_section_mock = AsyncMock(return_value=int)

        model_network_mock = Mock()
        model_network_mock.create_cross_section = create_cross_section_mock
        model_network_mock.cross_sections = Gio.ListStore.new(ModelCrossSection)
        model_network_mock.cross_sections.append(model_cross_section)

        network = Network(model_network_mock)

        self.assertEqual(network.cross_sections.get_n_items(), 1)

        view_model_cs = network.cross_sections.get_item(0)
        self.assertEqual(view_model_cs.id, "My id")
        self.assertEqual(view_model_cs.lanes, 5)

        await network.create_cross_section("my name", Location(0, 0), CrossSectionType.COMBINED)

        create_cross_section_mock.assert_awaited()


if __name__ == '__main__':
    unittest.main()
