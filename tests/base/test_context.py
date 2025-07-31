"""TODO"""
import asyncio
import unittest

from gi.events import GLibEventLoopPolicy

import common
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context


class ContextTestCase(unittest.TestCase):
    def setUp(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ContextTestCase().test())
        loop.run_until_complete(task)

    async def test(self) -> None:
        await self.projects()
    async def projects(self):
        context = Context()
        await context.load()
        proj_id = context.create_project("test_project", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "tests/base/test_project")
        self.assertEqual(context.projects.get_item(0).id, proj_id)
        self.assertEqual(context.projects.get_item(0).name, "test_project")
        context.create_project("test_project", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "tests/base/test_project")
        self.assertEqual(context.projects.get_n_items(), 2)
        self.assertEqual(context.projects.get_item(0).name, context.projects.get_item(1).name)
        self.assertNotEqual(context.projects.get_item(0).id, context.projects.get_item(1).id)



if __name__ == '__main__':
    unittest.main()