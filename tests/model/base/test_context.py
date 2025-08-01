"""TODO"""
import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context


class ContextTestCase(unittest.TestCase):

    def on_delete_async(feld, file, result, user_data):
        file.delete_finish(result)


    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ContextTestCase().start())
        loop.run_until_complete(task)

    async def start(self) -> None:
        await self.load()
        await self.projects()


    async def load(self):
        file = Gio.File.new_for_path("global_db")

        context1 = Context()
        await context1.load()

        await context1.load()
        proj_id = await context1.create_project(SimulatorType("dummy_json",
                                                              "JSON Dummy Simulator"),
                                                "simulation_file_path",
                                                "tests/base/test_project")
        # result manager is loaded from the db directly
        context2 = Context()
        await context2.load()
        self.assertIsNotNone(context2.projects.get_item(0))
        self.assertEqual(context2.projects.get_item(0).id, proj_id)

        file.delete_async(0, None, self.on_delete_async, None)



    async def projects(self):
        file = Gio.File.new_for_path("global_db")


        context = Context()
        await context.load()
        proj_id_1 = await context.create_project(SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "tests/base/test_project")
        self.assertEqual(context.projects.get_item(0).id, proj_id_1)
        proj_id_2 = await context.create_project(SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "tests/base/test_project")
        self.assertEqual(context.projects.get_n_items(), 2)
        self.assertNotEqual(context.projects.get_item(0).id, context.projects.get_item(1).id)


        await context.delete_project(proj_id_1)
        self.assertEqual(context.projects.get_item(0).id, proj_id_2)

        file.delete_async(0, None, self.on_delete_async, None)

        self.assertEqual(context.projects.get_item(0).id, proj_id_2)
