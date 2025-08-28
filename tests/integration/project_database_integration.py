import asyncio
import unittest

from gi.events import GLibEventLoopPolicy
from gi.repository import Gio, GLib

from sbaid.common.a_display import ADisplay
from sbaid.common.tag import Tag
from sbaid.model.algorithm.algorithm import Algorithm
from sbaid.model.algorithm.parameter_template import ParameterTemplate
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager
from sbaid.model.algorithm_configuration.parameter import Parameter
from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.context import Context as ModelContext
from sbaid.model.database.project_sqlite import ProjectSQLite
from sbaid.common.simulator_type import SimulatorType
from sbaid.model.network.network import Network
from sbaid.model.simulation.display import Display
from sbaid.model.simulation.input import Input
from sbaid.model.simulation.network_state import NetworkState
from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from tests.mock_simulator import MockSimulator


class AlgorithmImpl(Algorithm):
    def get_global_parameter_template(self) -> Gio.ListModel:
        store = Gio.ListStore.new(ParameterTemplate)
        store.append(ParameterTemplate("My global param", GLib.VariantType.new("s"),
                                       GLib.Variant.new_string("hi_global")))
        store.append(ParameterTemplate("My other global param", GLib.VariantType.new("d"),
                                       GLib.Variant.new_double(0.0)))
        return store

    def get_cross_section_parameter_template(self) -> Gio.ListModel:
        store = Gio.ListStore.new(ParameterTemplate)
        store.append(ParameterTemplate("My cross section param with default value",
                                       GLib.VariantType.new("s"), GLib.Variant.new_string("hi")))
        store.append(ParameterTemplate("My other cross section param", GLib.VariantType.new("d"),
                                       GLib.Variant.new_double(0.0)))
        return store

    def init(self, parameter_configuration_state: ParameterConfigurationState,
             network_state: NetworkState) -> None:
        self.__network_state = network_state

    def calculate_display(self, algorithm_input: Input) -> Display:
        display = Display()
        for cs_state in self.__network_state.cross_section_states:
            for lane in range(cs_state.lanes):
                display.set_a_display(cs_state.id, lane, ADisplay.SPEED_LIMIT_130)
        return display


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
        # await self.load_algo_config()
        # await self.algo_config_properties()
        # await self.algo_config_tag()
        await self.parameter_properties()
        # await self.parameter_tags()

    async def rename_project(self) -> None:
        global_file = Gio.File.new_build_filenamev([GLib.get_user_data_dir(), "sbaid", "global_db"])

        context1 = ModelContext()
        await context1.load()

        proj_id = await context1.create_project("project name",
                                                SimulatorType("dummy_json",
                                                              "JSON Dummy Simulator"),
                                                "simulation_file_path",
                                                "test_project")

        self.assertEqual(context1.projects.get_n_items(), 1)
        self.assertEqual(context1.projects.get_item(0).id, proj_id)
        self.assertEqual(context1.projects.get_item(0).name, "project name")

        context2 = ModelContext()
        await context2.load()

        self.assertIsNotNone(context2.projects.get_item(0))
        self.assertEqual(context2.projects.get_item(0).id, proj_id)
        self.assertEqual(context2.projects.get_n_items(), 1)

        await global_file.delete_async(0, None)
        project_file = Gio.File.new_for_path("test_project/db")
        project_dir = Gio.File.new_for_path("test_project")
        await project_file.delete_async(0, None)
        await project_dir.delete_async(0, None)

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


    async def parameter_properties(self) -> None:
        project_db_file = Gio.File.new_for_path("test_project_db")
        project_db = ProjectSQLite(project_db_file)
        await project_db.open()
        mock_sim = MockSimulator()
        algorithm = AlgorithmImpl()
        network = Network(mock_sim, project_db)
        await network.load()
        await network.load()

        parameter_config = ParameterConfiguration(network, project_db, "algo_config_id",
                                                  Gio.ListStore.new(Tag))
        parameter_config.set_algorithm(algorithm)
        await parameter_config.load()  # this causes the program to get stuck and not terminate

        self.assertEqual(parameter_config.parameters.get_n_items(),
                         2 + 2 * network.cross_sections.get_n_items())

        # same_project_db = ProjectSQLite(project_db_file)
        # same_mock_sim = MockSimulator()
        # same_algorithm = AlgorithmImpl()
        # same_network = Network(same_mock_sim, same_project_db)
        # await same_network.load()
        # await network.load()
        #
        # same_parameter_config = ParameterConfiguration(same_network, same_project_db, "algo_config_id",
        #                                           Gio.ListStore.new(Tag))
        # same_parameter_config.set_algorithm(same_algorithm)
        # await same_parameter_config.load()
        #
        # self.assertEqual(2 + 2 * same_network.cross_sections.get_n_items(),
        #                  same_parameter_config.parameters.get_n_items())
        await project_db_file.delete_async(0, None)

    async def parameter_tags(self) -> None:
        project_db_file = Gio.File.new_for_path("test_project_db")
        project_db = ProjectSQLite(project_db_file)
        await project_db.open()

        parameter = Parameter("param_name",
                              GLib.VariantType.new('s'),
                              GLib.Variant.new_string("my_param_string"),
                              None,
                              project_db,
                              "algo_config_id",
                              Gio.ListStore.new(Tag))
        parameter.add_tag(Tag("my_tag_id", "my_tag_name"))

        self.assertEqual("my_tag_name", parameter.selected_tags[0].name)

        same_parameter = Parameter("param_name",
                              GLib.VariantType.new('s'),
                              GLib.Variant.new_string("my_param_string"),
                              None,
                              project_db,
                              "algo_config_id",
                              Gio.ListStore.new(Tag))

        await same_parameter.load_from_db()

        self.assertEqual(1, len(same_parameter.selected_tags))
        self.assertEqual("my_tag_name", same_parameter.selected_tags[0].name)

        same_parameter.remove_tag(Tag("my_tag_id", "my_tag_name"))

        other_same_parameter = Parameter("param_name",
                                    GLib.VariantType.new('s'),
                                    GLib.Variant.new_string("my_param_string"),
                                    None,
                                    project_db,
                                    "algo_config_id",
                                    Gio.ListStore.new(Tag))

        await other_same_parameter.load_from_db()
        self.assertEqual(0, len(other_same_parameter.selected_tags))
