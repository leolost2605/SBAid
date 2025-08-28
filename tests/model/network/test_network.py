import sys
import unittest
from unittest import mock, skipIf
from unittest.mock import AsyncMock
import asyncio
from gi.repository import Gio
from sbaid.model.network.network import Network
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.network.parser_factory import ParserFactory
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from tests.mock_cross_section import MockCrossSection
from tests.mock_simulator import MockSimulator


class NetworkTest(unittest.TestCase):
    __mock_simulator = MockSimulator()
    __db = unittest.mock.Mock()
    __db.get_cross_section_name = unittest.mock.AsyncMock()
    __db.add_cross_section = unittest.mock.AsyncMock()
    __network = Network(__mock_simulator, __db)

    def test_factory_singleton(self):
        first_instance = ParserFactory()
        second_instance = ParserFactory()
        self.assertEqual(first_instance, second_instance)

    def test_load(self):
        """Uses async method to test loading of the network from the database."""
        asyncio.run(self._test_load())

    async def _test_load(self):
        """Tests the network's load method.
        Expected behavior: All model cross sections are created from simulator cross sections and
        their metadata loaded from the database."""
        await self.__network.load()
        self.assertEqual(self.__network.cross_sections.get_n_items(),
                         self.__network.cross_sections.get_n_items())
        self.assertEqual(self.__network.cross_sections.get_item(1).name, "cross_section_1")

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_import_from_file(self):
        asyncio.run(self._test_import_from_file())

    async def _test_import_from_file(self):
        """Mocks a Gio file to import cross sections from; or use one of the test ones (parsing
         has been tested; only relevant testing here is the actual method import_from_file).
         Expected output:
            dummy simulator: InvalidFormattingException because adding cross sections is not supported
            vissim simulator: return value (20,0)"""
        file = Gio.File.new_for_path("./tests/model/network/valid_input.csv")
        await self.__network.load()
        self.assertEqual(await self.__network.import_from_file(file), (20, 0))


    def test_load_from_db(self):
        asyncio.run(self._test_load_from_db())

    async def _test_load_from_db(self):
        """Expected behavior:
        cross section has value for hard shoulder active, b display active
        (simulator, name and id all come from simulator cross section)"""
        # use mock thing to mock values incoming from actual database
        project_db = unittest.mock.AsyncMock()
        project_db.get_cross_section_name = AsyncMock(return_value="database_name")
        project_db.get_cross_section_hard_shoulder_active = AsyncMock(return_value=True)
        project_db.get_cross_section_b_display_active = AsyncMock(return_value=True)

        mock_cs = MockCrossSection("id", "simulator_name", CrossSectionType.COMBINED, Location(0,0), 4)
        cross_section = CrossSection(mock_cs, project_db)
        await cross_section.load_from_db()
        self.assertEqual(cross_section.name, "database_name")
        self.assertEqual(cross_section.hard_shoulder_active, True)
        self.assertEqual(cross_section.b_display_active, True)
