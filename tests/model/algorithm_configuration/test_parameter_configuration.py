import unittest

from sbaid.model.algorithm_configuration.parameter_configuration import ParameterConfiguration
from sbaid.model.network.network import Network
from sbaid.model.simulator.dummy.dummy_simulator import DummySimulator
from sbaid.model.simulator.simulator import Simulator


class MyTestCase(unittest.TestCase):
    def test_parameter_configuration(self):
        assert True
        # TODO: Wait for working dummy then we can do this
        # simulator = DummySimulator()
        # network = Network(simulator)
        # parameter_config = ParameterConfiguration(network)


if __name__ == '__main__':
    unittest.main()
