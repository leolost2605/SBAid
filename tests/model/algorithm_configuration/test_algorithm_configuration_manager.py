"""This module contains unittest for the AlgorithmConfiguration class."""
import random
import unittest
from gi.repository import GLib

from sbaid.common.tag import Tag
from sbaid.model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager


class AlgorithmConfigurationManagerTest(unittest.TestCase):
    """This class tests teh algorithm configuration using pythons unittest."""

    test = GLib.VariantType.new('s')
    test_value = GLib.Variant.new_string('test_value')

    algo_config_manager = AlgorithmConfigurationManager(None)

    def test_create_tag(self):
        a = Tag(GLib.uuid_string_random(), "first_tag")
        b = Tag(GLib.uuid_string_random(), "second_tag")

        self.algo_config_manager.create_tag(a)
        self.algo_config_manager.create_tag(b)

    def delete_tag(self):
        all_tags = self.algo_config_manager.available_tags
        all_tags_ids = all_tags.get_ids()
        tag_id = random.choice(all_tags_ids)
        self.algo_config_manager.delete_tag(tag_id)

