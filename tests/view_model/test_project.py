import unittest


from sbaid.common.simulator_type import SimulatorType
from sbaid.model.project import Project as ModelProject
from sbaid.model.results.result_manager import ResultManager
from sbaid.view_model.project import Project


class ProjectTestCase(unittest.TestCase):
    def test_properties(self) -> None:
        res_manager = ResultManager()
        model_project = ModelProject("my_project_id", SimulatorType("dummy_json", "JSON Dummy"),
                                     "sim_path", "proj_file_path", res_manager)
        project = Project(model_project)
        self.assertEqual("my_project_id", project.id)
        self.assertEqual("Unknown Project Name", project.name)
        self.assertEqual("dummy_json", project.simulator_type.id)
        # last modified and created at are loaded from the database
