import sys
import unittest

from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.simulator.simulator_factory import SimulatorFactory
from sbaid.common.simulator_type import SimulatorType


class ProjectTestCase(unittest.TestCase):
    def test_get_simulator(self):
        sim_factory = SimulatorFactory()

        self.assertEqual(sim_factory.simulator_types.get_item(0).id, "dummy_json")

        type_dummy = SimulatorType("dummy_json", "JSON Dummy Simulator")
        self.assertIsInstance(sim_factory.get_simulator(type_dummy), DummySimulator)

        if sys.platform.startswith("win"):
            type_vissim = SimulatorType("com.ptvgroup.vissim", "PTV Vissim")
            from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator
            self.assertIsInstance(sim_factory.get_simulator(type_vissim), VissimSimulator)

            self.assertEqual(sim_factory.simulator_types.get_n_items(), 2)
        else:
            self.assertEqual(sim_factory.simulator_types.get_n_items(), 1)

if __name__ == '__main__':
    unittest.main()
