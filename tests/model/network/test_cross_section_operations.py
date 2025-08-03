import sys
import unittest
from unittest import mock
from unittest.mock import MagicMock
import asyncio

from sbaid.common import list_model_iterator
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
#if sys.platform.startswith("win"):
    #from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType


class CrossSectionOperationsTest(unittest.TestCase):
    __dummy_simulator = DummySimulator()
    if sys.platform.startswith("win"):
        #__vissim_simulator = VissimSimulator()
        __network = Network(__dummy_simulator, unittest.mock.Mock())
    #__network = Network(__dummy_simulator, unittest.mock.Mock())
    __sim_cross_section = SimulatorCrossSection()
    __cross_section: CrossSection = None

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_create_valid_cross_section(self):
        """Expected behavior:
            for dummy: operation not supported raised
            for vissim: an int, representing the position of the successfully added cross section
                        in the network's cross sections ListModel
        """
        asyncio.run(self._test_create_valid_cross_section())

    async def _test_create_valid_cross_section(self):
        position = await self.__network.create_cross_section("test_name",
                         Location(0,0), CrossSectionType.COMBINED)  #TODO: 0,0 is middle of the ocean; no cross sections
        self.assertEqual(self.__network.cross_sections.get_item(position), "test_name")
        self.__cross_section = self.__network.cross_sections.get_item(position)


    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_create_invalid_coordinates_cross_section(self):
        """invalid in a not-on-the-route sense
         Expected behavior:
            for dummy: raised operation not supported error
            for vissim: raised error in simulator
         """
        asyncio.run(self._test_create_invalid_coordinates_cross_section())

    async def _test_create_invalid_coordinates_cross_section(self):
        with self.assertRaises(Exception):
            await self.__network.create_cross_section("test_name", Location(0, 0),
                                                      CrossSectionType.COMBINED)

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_delete_cross_section(self):
        """Expected behavior:
        for dummy: operation not supported error
        for vissim: cross section no longer in cross sections listmodel (check separately from move operation)
        """
        asyncio.run(self._test_delete_cross_section())

    async def _test_delete_cross_section(self):
        await self.__network.delete_cross_section(self.__cross_section.id)
        deleted: bool = True
        for cs in list_model_iterator(self.__network.cross_sections):
            if cs.id == self.__cross_section.id:
                deleted = False
        self.assertEqual(True, deleted)

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_move_cross_section_valid(self):
        """Expected behavior:
        for dummy: operation not supported error
        for vissim: cross section has new location (check separately from move operation)
        """
        asyncio.run(self._test_move_cross_section_valid())

    async def _test_move_cross_section_valid(self):
        await self.__network.move_cross_section(self.__cross_section.id, Location(50.268010,8.663893))
        self.assertEqual(self.__cross_section.location, Location(50.268010,8.663893))

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_move_cross_section_invalid(self):
        """Expected behavior:
            for dummy: operation not supported error
            for vissim: error in simulator
        """
        asyncio.run(self._test_move_cross_section_invalid())

    async def _test_move_cross_section_invalid(self):
        await self.__network.move_cross_section(self.__cross_section.id, Location(0,0))  # 0,0 illegal bcs ocean
        self.assertEqual(self.__cross_section.location, Location(50.268010,8.663893))  #shouldn't change

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_rename_cross_section(self):
        """Expected behavior:
        for dummy: operation not supported error (?)
        for vissim: check name from id, see if == new name"""
        asyncio.run(self._test_rename_cross_section())

    async def _test_rename_cross_section(self):
        self.__cross_section.name = "changed name"
        self.assertEqual(self.__cross_section.name, "changed name")

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_set_b_display(self):
        """Set to true and then to false to test both cases idk
        Expected behavior:
            for dummy: operation not supported error
            for vissim: new value is given value"""
        self.__cross_section.b_display_active = True
        self.assertEqual(self.__cross_section.b_display_active, True)

    @unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
    def test_set_hard_shoulder_status(self):
        """Set to true and then to false to test both cases idk
        Expected behavior:
            for dummy: operation not supported error
            for vissim: new value is given value"""
        self.__cross_section.hard_shoulder_active = True
        self.assertEqual(self.__cross_section.hard_shoulder_active, True)

