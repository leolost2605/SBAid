"""This module contains unittests for the Context class."""
import asyncio
import unittest

from gi.events import GLibEventLoopPolicy

import sbaid.common
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context


class ContextTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def test_create_project(self):
        context = Context()
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())

        loop = asyncio.get_event_loop()

        task = loop.create_task(context.load())
        loop.run_until_complete(task)

        pr_id = context.create_project("my_other_name", SimulatorType("dummy simulator", "Dummy Simulator"),
                               "my_simulation_file_path", "my_project_file_path")

        self.assertEqual(2, context.projects.get_n_items())
