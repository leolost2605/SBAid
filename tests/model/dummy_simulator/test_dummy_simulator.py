"""This module contains unittests for the Display class."""
import asyncio
import unittest
from itertools import count
from typing import Callable

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio

from common import list_model_iterator
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator, EndOfSimulationException


class DisplayTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def setUp(self) -> None:
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(DisplayTestCase().test())
        loop.run_until_complete(task)

    async def test(self) -> None:
        await self.simple()
        await self.reset()
        await self.load_different_file()
        await self.run_too_long()

    async def simple(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("test.json")
        await sim.init_simulation()
        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 131.9)
        await sim.continue_simulation(1)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 130.3)

    async def reset(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("test.json")
        await sim.init_simulation()
        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 131.9)
        await sim.continue_simulation(1)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 130.3)

        await sim.stop_simulation()
        await sim.init_simulation()

        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 131.9)
        await sim.continue_simulation(1)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        self.assertEqual(fetched_input.get_average_speed("cs2", 0), 130.3)

    async def load_different_file(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("test.json")
        # self.assertRaises(FileNotFoundError, await sim.measure())

        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 4)
        await sim.continue_simulation(1)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_traffic_volume("cs1", 0), 2)
        other_file = Gio.File.new_for_path("test2.json")
        # self.assertRaises(RuntimeError, await sim.load_file(other_file))

    async def run_too_long(self) -> None:
        self.assertTrue(True)
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("test.json")
        await sim.init_simulation()
        await sim.load_file(cur_file)
        # self.assertRaises(EndOfSimulationException, await sim.continue_simulation(2))


