"""This module contains unittests for the Simulation Manager class."""

import unittest
import uuid

from sbaid.model.algorithm_configuration.algorithm_configuration_manager import AlgorithmConfigurationManager
from sbaid.model.network.network import Network
from sbaid.model.results.result_manager import ResultManager
from sbaid.model.simulation_manager import SimulationManager
from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.simulator.simulator import Simulator


class SimulationManagerTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def test_start(self):
        project_name = str(uuid.uuid4())
        config_id = str(uuid.uuid4())
        simulator = Simulator()
        network = Network(simulator)
        result_manager = ResultManager()
        observer = SimulationObserver()
        algo_config = AlgorithmConfigurationManager(config_id, network)

        sim_manager = SimulationManager(project_name, algo_config, network,
                                        simulator, result_manager, observer)
        sim_manager.start()
