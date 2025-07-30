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
        context.create_project("test_project", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "tests/base/test_project")
        new_context = Context()
        await new_context.load()
        contains_project = any(project.name == "tes_project" for project in filter(
            lambda project: project.name, common.list_model_iterator(new_context.projects)))
        print(any(project.name == "tes_project" for project in filter(
            lambda project: project.name, common.list_model_iterator(new_context.projects))))

        self.assertTrue(contains_project)
        # context.projects


if __name__ == '__main__':
    unittest.main()