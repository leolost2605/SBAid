import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio

from sbaid.model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager
from sbaid.model.database.project_sqlite import ProjectSQLite
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.database.global_sqlite import GlobalSQLite
from sbaid.model.network.network import Network
from sbaid.model.project import Project
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator


class ProjectDatabaseTestCase(unittest.TestCase):
    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectDatabaseTestCase().start())
        loop.run_until_complete(task)
        asyncio.set_event_loop_policy(None)

    async def start(self) -> None:
        # await self.rename_project()
        await self.load_algo_config()
        await self.algo_config_properties()
        await self.algo_config_tag()

    async def rename_project(self) -> None:
        project_db_file = Gio.File.new_for_path("test_project_db")
        project_db = ProjectSQLite(project_db_file)
        global_db_file = Gio.File.new_for_path("test_global_db")
        global_db = GlobalSQLite(global_db_file)
        await project_db.open()
        result_manager = ResultManager(global_db)
        project = Project("my_project_id", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                          "my_sim_file_path",
                          "project_file_path",
                          result_manager)
        project.name = "my_project_name"

        same_project = Project("my_project_id", SimulatorType("dummy_json", "JSON Dummy Simulator"),
                          "my_sim_file_path",
                          "project_file_path",
                          result_manager)

        self.assertEqual("Unknown Project Name", same_project.name)

        await same_project.load_from_db()

        self.assertEqual("my_project_name", same_project.name)

        await project_db_file.delete_async(0, None)
        await global_db_file.delete_async(0, None)

    async def load_algo_config(self) -> None:
        project_db_file = Gio.File.new_for_path("test_project_db")
        project_db = ProjectSQLite(project_db_file)
        await project_db.open()
        simulator = DummySimulator()
        network = Network(simulator, project_db)

        algo_config_manager = AlgorithmConfigurationManager(network, project_db)

        self.assertEqual(0, len(algo_config_manager.algorithm_configurations))
        await algo_config_manager.create_algorithm_configuration()
        self.assertEqual(1, len(algo_config_manager.algorithm_configurations))

        same_algo_config_manager = AlgorithmConfigurationManager(network, project_db)
        self.assertEqual(0, len(same_algo_config_manager.algorithm_configurations))
        await same_algo_config_manager.load()
        self.assertEqual(1, len(same_algo_config_manager.algorithm_configurations))

        await project_db_file.delete_async(0, None)

    async def algo_config_properties(self) -> None:
        project_db_file = Gio.File.new_for_path("test_project_db")
        project_db = ProjectSQLite(project_db_file)
        await project_db.open()
        simulator = DummySimulator()
        network = Network(simulator, project_db)

        algo_config_manager = AlgorithmConfigurationManager(network, project_db)

        await algo_config_manager.create_algorithm_configuration()

        algo_config_manager.selected_algorithm_configuration_id = (
            algo_config_manager.algorithm_configurations[0].id)

        same_algo_config_manager = AlgorithmConfigurationManager(network, project_db)
        self.assertEqual(0, len(same_algo_config_manager.algorithm_configurations))
        await same_algo_config_manager.load()
        self.assertEqual(1, len(same_algo_config_manager.algorithm_configurations))

        self.assertEqual(algo_config_manager.algorithm_configurations[0].id,
                         same_algo_config_manager.selected_algorithm_configuration_id)

        await project_db_file.delete_async(0, None)

    async def algo_config_tag(self) -> None:
        project_db_file = Gio.File.new_for_path("test_project_db")
        project_db = ProjectSQLite(project_db_file)
        await project_db.open()
        simulator = DummySimulator()
        network = Network(simulator, project_db)

        algo_config_manager = AlgorithmConfigurationManager(network, project_db)

        await algo_config_manager.create_tag("my_tag")
        self.assertEqual(1, len(algo_config_manager.available_tags))

        same_algo_config_manager = AlgorithmConfigurationManager(network, project_db)

        await same_algo_config_manager.load()

        self.assertEqual(1, len(same_algo_config_manager.available_tags))

        tag_id = same_algo_config_manager.available_tags[0].tag_id
        same_algo_config_manager.delete_tag(tag_id)  # uses run_coro_in_background

        other_same_algo_config_manager = AlgorithmConfigurationManager(network, project_db)

        await other_same_algo_config_manager.load()

        self.assertEqual(0, len(other_same_algo_config_manager.available_tags))

        await project_db_file.delete_async(0, None)

