"""This module contains unit tests for the cross section csv parser."""
import sys
import asyncio
import unittest

from gi.repository import Gio
from gi.events import GLibEventLoopPolicy
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.network.csv_cross_section_parser import CSVCrossSectionParser
from sbaid.common.location import Location


class CsvParserTest(unittest.TestCase):
    """This class tests the csv parser using pythons unittest."""
    __added_cross_sections = []

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_file_type_guesser(self):
        parser = CSVCrossSectionParser()
        self.assertEqual(parser.can_handle_file("./tests/model/network/valid_input.csv"), True)

    def test_make_parsing_async(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._test_valid_csv())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def _test_valid_csv(self):
        parser = CSVCrossSectionParser()
        file = Gio.File.new_for_path("./tests/model/network/valid_input.csv")
        self.assertEqual(await parser.foreach_cross_section(file, self.callbackthing), (20,0))

    async def callbackthing(self, name: str, location: Location, cs_type: CrossSectionType) -> bool:
        if f"{name}, {location}, {cs_type}" in self.__added_cross_sections:
            return False
        #TODO check for combination; wait until dummy things exist
        self.__added_cross_sections.append(f"{name}, {location}, {cs_type}")
        return True

    def test_empty_csv(self):
        pass

    def test_invalid_coordinate(self):
        pass

    def test_invalid_type(self):
        pass

    def test_invalid_columns(self):
        pass

