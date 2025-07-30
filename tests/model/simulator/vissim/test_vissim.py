import unittest
import os
import sys

from sbaid.model.simulator.vissim.vissim_network import InvalidLocationException

if not sys.platform.startswith("win"):
    raise unittest.SkipTest("Requires Windows")

from sbaid.common.a_display import ADisplay
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.common.location import Location
from sbaid.model.simulation.display import Display
from sbaid.model.simulator.vissim.vissim import VissimConnector


class VissimTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__connector = VissimConnector()

    async def asyncTearDown(self) -> None:
        await self.__connector.shutdown()

    async def test_load_file(self) -> None:
        path = os.path.abspath("./A5_sarah.inpx")
        route, cross_section_states = await self.__connector.load_file(path)
        self.assertEqual(len(cross_section_states), 35)

        aq_1 = cross_section_states[0]

        self.assertEqual(aq_1.id, "1")
        self.assertEqual(aq_1.type, CrossSectionType.DISPLAY)
        self.assertEqual(aq_1.lanes, 3)

        q_2 = cross_section_states[1]

        self.assertEqual(q_2.id, "261")

        mq_67 = cross_section_states[-1]

        self.assertEqual(mq_67.type, CrossSectionType.COMBINED)
        self.assertEqual(mq_67.lanes, 4)

        with self.subTest(msg="Test Remove Cross Section"):
            await self.__connector.remove_cross_section("1")
            await self.__connector.remove_cross_section("261")

            with self.assertRaises(KeyError):
                await self.__connector.remove_cross_section("5")

        with self.subTest(msg="Test Create Cross Section"):
            await self.__connector.create_cross_section(aq_1.location, CrossSectionType.COMBINED)

            with self.assertRaises(InvalidLocationException):
                await self.__connector.create_cross_section(Location(0, 0,), CrossSectionType.COMBINED)

        with self.subTest(msg="Test Simulation"):
            interval = 60

            time, duration = await self.__connector.init_simulation(interval)
            for i in range(int(duration / interval)):
                await self.__run_iteration(cross_section_states, interval)

    async def __run_iteration(self, states, interval):
        await self.__connector.continue_simulation(interval)
        algo_input = await self.__connector.measure()
        display = Display()
        for cs in states:
            for lane_index in range(cs.lanes):
                speed = algo_input.get_average_speed(cs.id, lane_index)
                volume = algo_input.get_traffic_volume(cs.id, lane_index)
                if lane_index == 0:
                    display.set_a_display(cs.id, lane_index, ADisplay.CLOSED_LANE)
                else:
                    display.set_a_display(cs.id, lane_index, ADisplay.SPEED_LIMIT_100)
        await self.__connector.set_display(display)


if __name__ == '__main__':
    unittest.main()
