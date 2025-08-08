import unittest
from unittest.mock import Mock, AsyncMock

from gi.repository import Gio

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.algorithm_configuration.csv_parameter_parser import CSVParameterParser
from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.algorithm_configuration.parser_factory import ParserFactory


class MyTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.__db_mock = Mock()
        self.__db_mock.get_algorithm_configuration_name = AsyncMock(return_value="test_algorithm_configuration")
        self.__db_mock.get_script_path = AsyncMock(return_value="my script path")
        self.__db_mock.get_evaluation_interval = AsyncMock(return_value=15)
        self.__db_mock.get_display_interval = AsyncMock(return_value=30)
        self.__db_mock.set_evaluation_interval = AsyncMock()

    async def test_algorithm_configuration(self):
        config_id = "ac_id"

        sim = DummySimulator()
        network = Network(sim, self.__db_mock)

        algo_config = AlgorithmConfiguration(config_id, network, self.__db_mock,
                                             Gio.ListStore.new(Tag))

        self.assertEqual(algo_config.id, config_id)
        self.assertEqual(algo_config.name, "New Algorithm Configuration")
        self.assertEqual(algo_config.display_interval, 60)
        self.assertEqual(algo_config.evaluation_interval, 60)
        self.assertEqual(algo_config.script_path, None)

        await algo_config.load_from_db()

        self.assertEqual(algo_config.id, config_id)
        self.assertEqual(algo_config.name, "test_algorithm_configuration")
        self.assertEqual(algo_config.evaluation_interval, 15)
        self.assertEqual(algo_config.display_interval, 30)
        self.assertEqual(algo_config.script_path, "my script path")

        algo_config.evaluation_interval = 30

        self.assertEqual(algo_config.evaluation_interval, 30)

    def test_can_handle_file(self) -> None:
        parser_factory = ParserFactory()
        file = Gio.File.new_for_path("valid_parameter_config.csv")
        parser = parser_factory.get_parser(file)
        self.assertIsInstance(parser, CSVParameterParser)

    def test_singleton_parser_factory(self) -> None:
        factory_1 = ParserFactory()
        factory_2 = ParserFactory()
        self.assertEqual(factory_1, factory_2)


if __name__ == '__main__':
    unittest.main()
