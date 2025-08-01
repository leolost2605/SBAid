import unittest
from unittest import mock

from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.simulator.simulator_cross_section import SimulatorCrossSection


class CrossSectionOperationsTest(unittest.TestCase):
    __simulator = DummySimulator()
    __sim_cross_section = SimulatorCrossSection()

    def test_create_valid_cross_section(self):
        """Expected behavior:
            for dummy: operation not supported raised
            for vissim: an int, representing the position of the successfully added cross section
                        in the network's cross sections ListModel
        """
        network = Network(DummySimulator(), unittest.mock.Mock())
        print(network.route)
        pass

    def test_create_invalid_coordinates_cross_section(self):
        """invalid in a not-on-the-route sense
         Expected behavior:
            for dummy: raised operation not supported error
            for vissim: raised error in simulator
         """
        pass

    def test_delete_cross_section(self):
        """Expected behavior:
        for dummy: operation not supported error
        for vissim: cross section no longer in cross sections listmodel (check separately from move operation)
        """
        pass

    def test_move_cross_section_valid(self):
        """Expected behavior:
        for dummy: operation not supported error
        for vissim: cross section has new location (check separately from move operation)
        """
        pass

    def test_move_cross_section_invalid(self):
        """TODO: combine maybe
        Expected behavior:
            for dummy: operation not supported error
            for vissim: error in simulator (check for compatibility before moving? - qualitätssicherung)
        """
        pass

    def test_rename_cross_section(self):
        """Expected behavior:
        for dummy: operation not supported error (?)
        for vissim: check name from id, see if == new name"""
        pass

    def test_set_b_display(self):
        """set to true and then to false to test both cases idk
        Expected behavior:
            for dummy: operation not supported error
            for vissim: new value is given value"""
        #self.__simulator.
        pass

    def test_set_hard_shoulder_status(self):
        """set to true and then to false to test both cases idk
        Expected behavior:
            for dummy: operation not supported error
            for vissim: new value is given value"""
        pass

    def test_load_from_db(self):
        """Expected behavior:
        cross section has value for hard shoulder active, b display active
        (simulator, name and id all come from simulator cross section)"""

        pass