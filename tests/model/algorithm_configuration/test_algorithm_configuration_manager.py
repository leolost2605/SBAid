"""This module contains unittest for the AlgorithmConfiguration class."""
import random
import unittest
from unittest.mock import Mock, AsyncMock

from sbaid.model.algorithm_configuration.algorithm_configuration_manager import \
    AlgorithmConfigurationManager
from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.__db_mock = AsyncMock()
        self.__db_mock.get_all_algorithm_configuration_ids = AsyncMock(return_value=["1", "2"])
        self.__db_mock.get_selected_algorithm_configuration_id = AsyncMock(return_value="1")
        self.__db_mock.get_algorithm_configuration_name = AsyncMock(return_value="test_algorithm_configuration")
        self.__db_mock.get_script_path = AsyncMock(return_value="my script path")
        self.__db_mock.get_evaluation_interval = AsyncMock(return_value=15)
        self.__db_mock.get_display_interval = AsyncMock(return_value=30)
        self.__db_mock.add_algorithm_configuration = AsyncMock()
        self.__db_mock.remove_algorithm_configuration = AsyncMock()
        self.__db_mock.set_selected_algorithm_configuration_id = AsyncMock()
        self.__db_mock.add_tag = AsyncMock()
        self.__db_mock.remove_tag = AsyncMock()

    async def test_algo_config_manager(self):
        sim = DummySimulator()
        network = Network(sim, self.__db_mock)
        manager = AlgorithmConfigurationManager(network, self.__db_mock)

        await manager.load()

        self.assertEqual(manager.algorithm_configurations.get_n_items(), 2)
        self.assertEqual(manager.selected_algorithm_configuration_id, "1")
        self.assertEqual(manager.algorithm_configurations.get_item(0).id, "1")
        self.assertEqual(manager.algorithm_configurations.get_item(0).name, "test_algorithm_configuration")

        manager.selected_algorithm_configuration_id = "2"

        self.assertEqual(manager.selected_algorithm_configuration_id, "2")

        pos = await manager.create_algorithm_configuration()

        self.assertEqual(pos, 2)
        self.assertEqual(manager.algorithm_configurations.get_n_items(), 3)
        self.assertEqual(manager.algorithm_configurations.get_item(2).name, "New Algorithm Configuration")

        manager.selected_algorithm_configuration_id = "1"
        self.assertEqual(manager.selected_algorithm_configuration_id, "1")

        manager.delete_algorithm_configuration("1")

        self.assertEqual(manager.algorithm_configurations.get_n_items(), 2)
        self.assertEqual(manager.algorithm_configurations.get_item(0).id, "2")
        self.assertNotEqual(manager.algorithm_configurations.get_item(1).id, "1")
        self.assertEqual(manager.selected_algorithm_configuration_id, "2")

        tag_pos = await manager.create_tag("my tag")

        self.assertEqual(tag_pos, 0)
        self.assertEqual(manager.available_tags.get_n_items(), 1)
        self.assertEqual(manager.available_tags.get_item(0).name, "my tag")

        manager.delete_tag(manager.available_tags.get_item(0).tag_id)

        self.assertEqual(manager.available_tags.get_n_items(), 0)


if __name__ == '__main__':
    unittest.main()
