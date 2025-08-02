import unittest
from unittest import mock
import asyncio

from gi.repository import Gio
from sbaid.model.network.network import Network
from sbaid.model.network.parser_factory import ParserFactory
from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator


class NetworkTest(unittest.TestCase):

    __network = Network(VissimSimulator(), unittest.mock.Mock())

    def test_factory_singleton(self):
        first_instance = ParserFactory()
        second_instance = ParserFactory()
        self.assertEqual(first_instance, second_instance)

    def test_load(self):
        """Uses async method to test loading of the network from the database."""
        asyncio.run(self._test_load())

    async def _test_load(self):
        """Mocks the database and loads stuff from it"""

    def test_import_from_file_valid(self):
        asyncio.run(self._test_import_from_file_valid())

    async def _test_import_from_file_valid(self):
        """Mocks a Gio file to import cross sections from; or use one of the test ones (parsing
         has been tested; only relevant testing here is the actual method import_from_file)"""
        file = Gio.File.new_for_path("valid_input.csv")
        self.assertEqual(await self.__network.import_from_file(file), (20,0))

    #TODO: se calhar ainda testar invalido

    def test_route(self):
        asyncio.run(self._test_route())

    async def _test_route(self):
        """Checks if getting a route from a simulator works.
        Expected behaviour:
            dummy: list of (0,0) locations or None
            vissim: Route instance of network class has a ListModel of Location objects.
        """
