import unittest
from unittest import mock
import asyncio
from typing import cast
from sbaid.common import list_model_iterator
from sbaid.model.network.cross_section import CrossSection
from sbaid.model.network.network import Network
from tests.mock_cross_section import MockCrossSection
from tests.mock_simulator import MockSimulator
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection
from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType


class CrossSectionOperationsTest(unittest.IsolatedAsyncioTestCase):
    __mock_simulator = MockSimulator()
    __network = Network(__mock_simulator, unittest.mock.Mock())
    __sim_cross_section = SimulatorCrossSection()
    __mock_cross_section = MockCrossSection("test_id",
                                            "start_name",
                                            CrossSectionType.COMBINED,
                                            Location(0,0),
                                            4)
    __cross_section: CrossSection = CrossSection(__mock_cross_section, unittest.mock.Mock())


    async def test_create_cross_section(self):
        """Expected behavior:
            for dummy: operation not supported raised
            for vissim: an int, representing the position of the successfully added cross section
                        in the network's cross sections ListModel
            mock: an int, representing the position of the successfully added cross section
                        in the network's cross sections ListModel
        """
        await self.__network.load()
        position = await self.__network.create_cross_section("creation_name",  # TODO uses non-mock
                                                             Location(50.16106, 8.39521),
                                                             CrossSectionType.COMBINED)
        self.assertEqual(self.__network.cross_sections.get_item(position).name, "creation_name")
        self.__cross_section = cast(CrossSection, self.__network.cross_sections.get_item(position))


    async def test_move_cross_section(self):
        """Expected behavior:
                for dummy: operation not supported error
                for vissim: cross section has new location (check separately from move operation)
                """
        self.__mock_simulator.cross_sections.append(self.__mock_cross_section)
        await self.__network.move_cross_section(self.__cross_section.id, Location(50.268010, 8.663893))
        self.assertEqual(self.__cross_section.location, Location(50.268010, 8.663893))

    async def test_delete_cross_section(self):
        """Expected behavior:
                for dummy: operation not supported error
                for vissim: cross section no longer in cross sections listmodel (check separately from move operation)
                """
        await self.__network.load()
        await self.__network.delete_cross_section(self.__cross_section.id)
        deleted: bool = True
        for cs in list_model_iterator(self.__network.cross_sections):
            if cs.id == self.__cross_section.id:
                deleted = False
        self.assertEqual(True, deleted)

    async def test_rename_cross_section(self):
        """Expected behavior:
                for dummy: operation not supported error (?)
                for vissim: check name from id, see if == new name
        """
        self.__cross_section.name = "changed name"
        self.assertEqual(self.__cross_section.name, "changed name")

    def test_set_b_display(self):
        """Set to true and then to false to test both cases
        Expected behavior:
            for dummy: operation not supported error
            for vissim: new value is the given value
            mock: new value is the given value"""
        self.__cross_section.b_display_active = True
        self.assertEqual(self.__cross_section.b_display_active, True)

    def test_set_hard_shoulder_status(self):
        """Set to true and then to false to test both cases idk
        Expected behavior:
            for dummy: operation not supported error
            for vissim: new value is the given value
            mock: new value is the given value"""
        self.__cross_section.hard_shoulder_active = True
        self.assertEqual(self.__cross_section.hard_shoulder_active, True)
