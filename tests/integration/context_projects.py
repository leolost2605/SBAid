import asyncio
import unittest

from gi.events import GLibEventLoopPolicy

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context as ModelContext
from sbaid.view_model.context import Context


class ContextProjectsTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ContextProjectsTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:
        await self.simple()

    async def simple(self):
        model_context = ModelContext()
        vm_context = Context(model_context)

        # TODO check for duplicate project id
        await vm_context.create_project("project_name_1",
                                  SimulatorType("dummy_json", "JSON Dummy"),
                                  "sim_file_path",
                                  "project_file_path")

        self.assertEqual(1, len(vm_context.projects))
        self.assertEqual(1, len(model_context.projects))

        await vm_context.create_project("project_name_2",
                                  SimulatorType("dummy_json", "JSON Dummy"),
                                  "sim_file_path",
                                  "project_file_path")

        self.assertEqual(2, len(model_context.projects))
        self.assertEqual(2, len(vm_context.projects))

        await vm_context.delete_project(vm_context.projects[0].id)

        self.assertEqual(1, len(model_context.projects))
        self.assertEqual(1, len(vm_context.projects))