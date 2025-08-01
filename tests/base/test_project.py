"""TODO"""
import asyncio
import unittest
from unittest import mock

from gi.events import GLibEventLoopPolicy
from gi.repository import GLib
from gi.repository import Gio

from model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager
from model.network.network import Network
from model.project import Project, AlgorithmConfigurationException
from model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.context import Context


class ProjectTestCase(unittest.TestCase):

    def on_delete_async(feld, file, result, user_data):
        file.delete_finish(result)


    def test(self):
        self.assertTrue(True)
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(ProjectTestCase().start())
        loop.run_until_complete(task)

    async def start(self) -> None:
        await self.start_simulation()


    async def start_simulation(self):
        context = mock.Mock()
        context.load()
        observer = mock.Mock()
        file = Gio.File.new_for_path("global_db")

        sim = DummySimulator()
        db = mock.Mock()
        network = Network(sim, db)
        algo_config_manager = AlgorithmConfigurationManager(network)
        algo_config = mock.Mock()
        algo_config.parameter_configuration = mock.Mock()
        # algo_config = algo_config_manager.create_algorithm_configuration()
        project = Project(GLib.uuid_string_random(),
                          SimulatorType("dummy_json", "JSON Dummy Simulator"),
                          "simulation_file_path", "tests/base/test_project",
                          algo_config_manager)
        await project.load()
        self.assertRaises(AlgorithmConfigurationException, project.start_simulation, observer)
        # algo_config.parameter_configuration = mock.Mock()
        project.algorithm_configuration_manager.algorithm_configurations.append(algo_config)
        project.algorithm_configuration_manager\
            .selected_algorithm_configuration_id = "my_config_id"
        simulation_manager = project.start_simulation(observer)
        await simulation_manager.start()

