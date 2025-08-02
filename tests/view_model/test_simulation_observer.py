import unittest

from gi.repository import GObject

from sbaid.view_model.simulation_observer import SimulationObserver


class SimulationObserverTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.progress_one = None
        self.error = None

    def test_signals(self):
        observer = SimulationObserver()
        observer.connect("progressed", self.__on_progressed)
        observer.connect("finished", self.__on_finished)
        observer.connect("failed", self.__on_failed)

        observer.update_progress(20.5)
        observer.update_progress(55.789)
        observer.finished("result id")
        observer.failed(GObject.Error.new_literal(5, 1, "my message"))

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
