import unittest
from gi.repository import Gio, GLib
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context

class ContextTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_load(self):
        global_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])

        context1 = Context()
        await context1.load()

        proj_id = await context1.create_project("project name",
                                                SimulatorType("dummy_json",
                                                              "JSON Dummy Simulator"),
                                                "simulation_file_path",
                                                "test_project")

        self.assertEqual(context1.projects.get_n_items(), 1)
        self.assertEqual(context1.projects.get_item(0).id, proj_id)
        self.assertEqual(context1.projects.get_item(0).name, "project name")

        context2 = Context()
        await context2.load()

        self.assertIsNotNone(context2.projects.get_item(0))
        self.assertEqual(context2.projects.get_item(0).id, proj_id)
        self.assertEqual(context2.projects.get_n_items(), 1)

        global_file.delete_async(GLib.PRIORITY_DEFAULT, None, self.__on_delete)

    async def test_projects(self):
        global_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])

        context = Context()
        await context.load()

        proj_id_1 = await context.create_project("my project name", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "test_project")

        self.assertEqual(context.projects.get_item(0).id, proj_id_1)

        proj_id_2 = await context.create_project("my other project name", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                               "simulation_file_path", "test_project")

        self.assertEqual(context.projects.get_n_items(), 2)
        self.assertNotEqual(context.projects.get_item(0).id, context.projects.get_item(1).id)

        await context.delete_project(proj_id_1)
        self.assertEqual(context.projects.get_item(0).id, proj_id_2)
        self.assertEqual(context.projects.get_n_items(), 1)

        global_file.delete_async(GLib.PRIORITY_DEFAULT, None, self.__on_delete)

    def __on_delete(self, source_object, result, user_data):
        try:
            source_object.delete_finish()
        except GLib.GError as e:
            raise e