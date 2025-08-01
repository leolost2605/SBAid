"""TODO"""
import sys
import unittest

from gi.repository import GLib
from model.simulator.dummy.dummy_simulator import DummySimulator
from model.simulator_factory import SimulatorFactory
from sbaid.common.simulator_type import SimulatorType


class ProjectTestCase(unittest.TestCase):

    def test_get_simulator(self):
        sim_factory = SimulatorFactory()

        type_dummy = SimulatorType("dummy_json", "JSON Dummy Simulator")

        if sys.platform.startswith("win"):
            type_vissim = SimulatorType("com.ptvgroup.vissim", "PTV Vissim")
            from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator
            self.assertEqual(VissimSimulator, type(sim_factory.get_simulator(type_vissim)))

        self.assertEqual(DummySimulator, type(sim_factory.get_simulator(type_dummy)))
