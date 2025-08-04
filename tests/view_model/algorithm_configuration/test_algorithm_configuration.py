import unittest

from unittest.mock import Mock

from gi.repository import Gio

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.parameter import Parameter as ModelParameter
from sbaid.view_model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.view_model.network.cross_section import CrossSection


class AlgorithmConfigurationTestCase(unittest.TestCase):
    def test_algorithm_configuration(self):
        model_config_mock = Mock()
        model_config_mock.name = "my name"
        model_config_mock.parameter_configuration.parameters = Gio.ListStore.new(ModelParameter)

        network_mock = Mock()
        network_mock.cross_sections = Gio.ListStore.new(CrossSection)

        tags = Gio.ListStore.new(Tag)

        config = AlgorithmConfiguration(model_config_mock, network_mock, tags)

        self.assertEqual(config.name, "my name")


if __name__ == '__main__':
    unittest.main()
