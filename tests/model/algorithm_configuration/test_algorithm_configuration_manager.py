"""This module contains unittest for the AlgorithmConfiguration class."""
import random
import unittest
from unittest.mock import MagicMock, mock_open

from gi.repository import GLib

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager


class AlgorithmConfigurationManagerTest(unittest.TestCase):
    """This class tests teh algorithm configuration using pythons unittest."""

    def setUp(self):
        self.test = GLib.VariantType.new('s')
        self.test_value = GLib.Variant.new_string('test_value')
        self.mock_network = MagicMock(name="MockNetwork")
        self.algo_config_manager = AlgorithmConfigurationManager(self.mock_network)

    def test_create_tag(self):
        a = Tag(GLib.uuid_string_random(), "first_tag")
        b = Tag(GLib.uuid_string_random(), "second_tag")

        self.algo_config_manager.create_tag(a)
        self.algo_config_manager.create_tag(b)

        tags = self.algo_config_manager.available_tags
        self.assertIn(a.id, tags.get_ids())
        self.assertIn(b.id, tags.get_ids())

    def test_delete_tag(self):
        a = Tag(GLib.uuid_string_random(), "temp_tag")
        self.algo_config_manager.create_tag(a)

        all_tags = self.algo_config_manager.available_tags
        all_tags_ids = all_tags.get_ids()
        self.assertIn(a.id, all_tags_ids)

        self.algo_config_manager.delete_tag(a.id)
        all_tags_after = self.algo_config_manager.available_tags.get_ids()
        self.assertNotIn(a.id, all_tags_after)

    def test_create_algorithm_configuration(self):
        pass

    def test_delete_algorithm_configuration(self):
        pass

if __name__ == '__main__':
    unittest.main()