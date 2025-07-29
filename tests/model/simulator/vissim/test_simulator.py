import unittest
import sys

from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator

@unittest.skipUnless(sys.platform.startswith("win"), "Requires Windows")
class SimulatorTestCase(unittest.TestCase):
    def setUp(self):
        self.simulator = VissimSimulator()


if __name__ == '__main__':
    unittest.main()
