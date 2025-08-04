import unittest
from unittest.mock import Mock

from gi.repository import GObject

from sbaid.model.simulation_manager import SimulationManager
from sbaid.model.simulation_observer import SimulationObserver as ModelSimulationObserver
from sbaid.view_model.simulation import Simulation
from sbaid.view_model.simulation_observer import SimulationObserver


class SimulationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.progress_one = None
        self.error = None

    def test_signals(self):
        algo_config = Mock()
        network = Mock()
        simulator = Mock()
        result_manager = Mock()
        observer = ModelSimulationObserver()
        manager = SimulationManager("proj_name", algo_config, network, simulator,
                                    result_manager, observer)
        vm_observer = SimulationObserver()
        simulation = Simulation(manager, vm_observer)

        simulation.connect("progressed", self.__on_progressed)
        simulation.connect("finished", self.__on_finished)
        simulation.connect("failed", self.__on_failed)

        vm_observer.update_progress(20.5)
        vm_observer.update_progress(55.789)
        vm_observer.finished("result id")
        vm_observer.failed(GObject.Error.new_literal(5, 1, "my message"))

        self.assertEqual(self.progress_one, 20.5)
        self.assertEqual(self.progress_two, 55.789)
        self.assertEqual(self.result, "result id")
        self.assertEqual(self.error.message, "my message")

    def __on_progressed(self, obj, progress):
        if self.progress_one is None:
            self.progress_one = progress

        self.progress_two = progress

    def __on_finished(self, obj, result_id):
        self.result = result_id

    def __on_failed(self, obj, error):
        self.error = error

if __name__ == '__main__':
    unittest.main()
