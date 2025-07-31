"""This module contains unit tests for the cross section csv parser."""
import sys
import asyncio
import unittest
from unittest import mock

from gi.repository import Gio
from gi.events import GLibEventLoopPolicy
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.network.network import Network
from sbaid.model.network.csv_cross_section_parser import CSVCrossSectionParser
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.common.location import Location
from sbaid.model.network.network import FailedCrossSectionCreationException

class CsvParserTest(unittest.TestCase):
    """This class tests the csv parser using pythons unittest."""
    __background_tasks = set()

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_file_type_guesser(self):
        parser = CSVCrossSectionParser()
        self.assertEqual(parser.can_handle_file("valid_input.csv"), True)

    def test_valid_parsing(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._test_valid_parsing())
        loop.run_until_complete(task)

    async def _test_valid_parsing(self):
        self.assertRaises(FailedCrossSectionCreationException, self.__valid_csv_callback_func)

    async def __valid_csv_callback_func(self):
        parser = CSVCrossSectionParser()
        file = Gio.File.new_for_path("valid_input.csv")
        await parser.foreach_cross_section(file, self.foreach_func_callback_func)

    def test_empty_csv(self):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._test_empty_csv())
        loop.run_until_complete(task)

    async def _test_empty_csv(self):
        self.assertRaises(FailedCrossSectionCreationException, self.__empty_csv_callback_func)

    async def __empty_csv_callback_func(self):
        parser = CSVCrossSectionParser()
        file = Gio.File.new_for_path("empty_input.csv")
        await parser.foreach_cross_section(file, self.foreach_func_callback_func)

    async def foreach_func_callback_func(self, name: str, location: Location, cross_section_type: CrossSectionType) -> bool:
        network = Network(DummySimulator(), unittest.mock.Mock())
        await network.create_cross_section(name, location, cross_section_type)

    def test_invalid_coordinate(self):
        pass

    def test_invalid_type(self):
        pass

    def test_invalid_columns(self):
        pass

