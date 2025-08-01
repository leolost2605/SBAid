"""This module contains unit tests for the cross section csv parser."""
import sys
import asyncio
import unittest
from unittest import mock

from gi.repository import Gio
from gi.events import GLibEventLoopPolicy
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.network.network import Network
from sbaid.model.network.csv_cross_section_parser import CSVCrossSectionParser, InvalidFileFormattingException
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.common.location import Location
from sbaid.model.network.network import FailedCrossSectionCreationException

class CsvParserTest(unittest.TestCase):
    """This class tests the csv parser using pythons unittest."""
    __background_tasks = set()

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_file_type_guesser(self):
        parser = CSVCrossSectionParser()
        self.assertEqual(parser.can_handle_file("./tests/model/network/valid_input.csv"), True)

    async def _testing_callback_func(self, path: str):
        parser = CSVCrossSectionParser()
        file = Gio.File.new_for_path(path)
        await parser.foreach_cross_section(file, self.foreach_func_callback_func)

    async def foreach_func_callback_func(self, name: str, location: Location,
                                         cross_section_type: CrossSectionType) -> bool:
        """Unit testing with dummy simulator so no upload of the vissim simulation
        files to github is needed"""
        network = Network(DummySimulator(), unittest.mock.Mock())
        return await network.create_cross_section(name, location, cross_section_type) is not None  #???? como check se raised um error ou returned algo?


    def test_valid_parsing(self):
        asyncio.run(self._test_valid_parsing())

    async def _test_valid_parsing(self):
        """Expected behavior with dummy simulator: skipping the first row of file and attempting
        creation of the second one, raising a FailedCrossSectionCreationException
        Expected behavior with vissim simulator: 20 added cross sections and 0 skipped ones"""
        with self.assertRaises(FailedCrossSectionCreationException):
            await self._testing_callback_func("./tests/model/network/valid_input.csv")


    def test_empty_csv(self):
        asyncio.run(self._test_empty_csv())

    async def _test_empty_csv(self):
        with self.assertRaises(InvalidFileFormattingException):
            await self._testing_callback_func("./tests/model/network/empty_sheet.csv")


    def test_invalid_coordinates(self):
        asyncio.run(self._test_invalid_coordinates())

    async def _test_invalid_coordinates(self):
        """Expected behavior with dummy simulator: skipping the first row of file and attempting
        creation of the second one, raising a FailedCrossSectionCreationException
        Expected behavior with vissim simulator: 14 added cross sections and 5 skipped ones"""
        with self.assertRaises(FailedCrossSectionCreationException):
            await self._testing_callback_func("./tests/model/network/invalid_coordinates.csv")


    def test_invalid_types(self):
        asyncio.run(self._test_invalid_types())

    async def _test_invalid_types(self):
        """Expected behavior with dummy simulator: skipping the first row of file and attempting
        creation of the second one, raising a FailedCrossSectionCreationException
        Expected behavior with vissim simulator: 15 added cross sections and 4 skipped ones"""
        with self.assertRaises(FailedCrossSectionCreationException):
            await self._testing_callback_func("./tests/model/network/invalid_types.csv")

    def test_invalid_columns(self):
        asyncio.run(self._test_invalid_columns())
        pass

    async def _test_invalid_columns(self):
        """Expected behavior with dummy simulator: skipping the first row of file and attempting
        creation of the second one, raising a FailedCrossSectionCreationException
        Expected behavior with vissim simulator: 11 added cross sections and 8 skipped ones"""
        with self.assertRaises(FailedCrossSectionCreationException):
            await self._testing_callback_func("./tests/model/network/invalid_columns.csv")

