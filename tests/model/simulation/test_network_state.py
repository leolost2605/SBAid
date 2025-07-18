"""This module contains unittests for the NetworkState class."""

import unittest
from typing import List

from sbaid.common.location import Location
from sbaid.common.cross_section_type import CrossSectionType
from sbaid.model.simulation.cross_section_state import CrossSectionState
from sbaid.model.simulation.network_state import NetworkState


class NetworkStateTest(unittest.TestCase):
    """This class tests the network state using pythons unittest."""

    def test_empty_network_state(self):
        """Test a network state with no cross sections."""
        network_state = NetworkState([],[])
        self.assertEqual(network_state.route.get_n_items(), 0)
        self.assertEqual(network_state.cross_section_states.get_n_items(), 0)

    def test_route(self):
        """Test a network state """
        route: List[Location] = [Location(0, 0), Location(0, 1), Location(1, 0),
                                 Location(1, 1)]
        network_state = NetworkState(route, [])
        self.assertEqual(network_state.route.get_n_items(), 4)
        self.assertEqual(network_state.route.get_item(0), Location(0, 0))
        self.assertEqual(network_state.route.get_item(1), Location(0, 1))
        self.assertEqual(network_state.route.get_item(2), Location(1, 0))
        self.assertEqual(network_state.route.get_item(3), Location(1, 1))

    def test_cross_section_states(self):
        cs1: CrossSectionState = CrossSectionState("my_cs_id", CrossSectionType.COMBINED,
                                                   4, True, False)
        cs2: CrossSectionState = CrossSectionState("my_cs_id2", CrossSectionType.COMBINED,
                                                   4, True, False)
        network_state = NetworkState([], [cs1, cs2])

        self.assertEqual(network_state.route.get_n_items(), 0)
        self.assertEqual(network_state.cross_section_states.get_n_items(), 2)
        self.assertEqual(network_state.cross_section_states.get_item(0).cross_section_state_id, "my_cs_id")
        self.assertEqual(network_state.cross_section_states.get_item(1).cross_section_state_id, "my_cs_id2")
