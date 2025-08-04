"""This module consists of the CSV parameter parser and InvalidFileFormattingException,
which can be raised during file parsing and handling."""
import asyncio
import sys
import unittest
from unittest.mock import Mock
from gi.repository import Gio

from sbaid.model.algorithm_configuration.csv_parameter_parser import CSVParameterParser
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator


class CsvParameterParserTest(unittest.TestCase):
    """This class tests the csv parser using pythons unittest."""
    __background_tasks = set()

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_file_type_guesser(self):
        parser = CSVParameterParser()
        self.assertEqual(parser.can_handle_file("valid_parameter_config.csv"), True)

    async def _testing_callback_func(self, path: str):
        parser = CSVParameterParser()
        file = Gio.File.new_for_path(path)
        await parser.for_each_parameter(file, self.foreach_func_callback_func)

    async def foreach_func_callback_func(self, name: str) -> bool:
        network = Network(DummySimulator(), unittest.mock.Mock())
        parameter_configuration = ParameterConfiguration(network)
        await parameter_configuration.import_from_file()


    def test_valid_parsing(self):
        asyncio.run(self._test_valid_parsing())

    async def _test_valid_parsing(self):
        with self.assertRaises(Exception):
            await self._testing_callback_func("valid_parameter_config.csv")