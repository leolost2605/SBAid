"""This module contains unittests for the Display class."""
import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio

from model.simulator.dummy.dummy_simulator import DummySimulator


class DisplayTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def setUp(self) -> None:
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(DisplayTestCase().test())
        loop.run_until_complete(task)

    async def test(self) -> None:
        await self.simple_test()

    async def simple_test(self):
        sim = DummySimulator()

        cur_file = Gio.File.new_for_path("test.json")
        await sim.init_simulation()
        await sim.load_file(cur_file)
        fetched_input = await sim.measure()
        self.assertEqual(fetched_input.get_average_speed(), 127.45)

