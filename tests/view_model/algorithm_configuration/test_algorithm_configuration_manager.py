import unittest
from unittest.mock import Mock

from gi.repository import Gio

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.view_model.algorithm_configuration.algorithm_configuration_manager import \
    AlgorithmConfigurationManager


class AlgorithmConfigurationManagerTestCase(unittest.TestCase):
    def test_algorithm_configuration_manager(self):
        manager_mock = Mock()
        manager_mock.algorithm_configurations = Gio.ListStore.new(AlgorithmConfiguration)
        manager_mock.available_tags = Gio.ListStore.new(Tag)

        network_mock = Mock()

        manager = AlgorithmConfigurationManager(manager_mock, network_mock)


if __name__ == '__main__':
    unittest.main()
