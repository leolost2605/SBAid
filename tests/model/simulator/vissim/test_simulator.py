import unittest

from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator


class SimulatorTestCase(unittest.TestCase):
    def setUp(self):
        self.simulator = VissimSimulator()


if __name__ == '__main__':
    unittest.main()
