import unittest
from unittest.mock import Mock
from gi.repository import Gio

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.project import Project as ModelProject
from sbaid.view_model.context import Context
from sbaid.view_model.project import Project


class ContextTestCase(unittest.TestCase):
    def test_simple(self):
        model_context = Mock()
        model_context.projects = Gio.ListStore.new(ModelProject)

        global_mock_db = unittest.mock.AsyncMock()
        res_manager = ResultManager(global_mock_db)
        my_model_project = ModelProject("my_project_id", SimulatorType("dummy_json", "JSON Dummy"),
                                     "sim_path", "proj_file_path", res_manager)
        model_context.projects.append(my_model_project)

        context = Context(model_context)
        # self.assertEqual(context.result_manager, res_manager)
        self.assertIsInstance(context.projects.get_item(0), Project)
        self.assertEqual("my_project_id", context.projects.get_item(0).id)

