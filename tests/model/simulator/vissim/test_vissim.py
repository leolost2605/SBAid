import unittest
import os

from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulator.vissim.vissim import VissimConnector


class VissimTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__connector = VissimConnector()

    async def asyncTearDown(self) -> None:
        await self.__connector.shutdown()

    async def test_load_file(self) -> None:
        path = os.path.abspath("./A5_sarah.inpx")
        cross_section_states = await self.__connector.load_file(path)
        self.assertEqual(len(cross_section_states), 48)

        mq_67 = cross_section_states[-1]

        self.assertEqual(mq_67.type, CrossSectionType.MEASURING)
        self.assertEqual(mq_67.lanes, 4)

        with self.subTest(msg="Test Remove Cross Section"):
            await self.__connector.remove_cross_section("11")


if __name__ == '__main__':
    unittest.main()
