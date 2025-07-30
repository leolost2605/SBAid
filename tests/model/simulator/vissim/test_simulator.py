import unittest
import sys

if not sys.platform.startswith("win"):
    raise unittest.SkipTest("Requires Windows")

from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator


class SimulatorTestCase(unittest.TestCase):
    def setUp(self):
        self.simulator = VissimSimulator()


if __name__ == '__main__':
    unittest.main()
