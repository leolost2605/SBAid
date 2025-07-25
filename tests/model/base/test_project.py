"""This module contains unittests for the Project class."""

import unittest
import uuid

from sbaid.common.simulator_type import SimulatorType
from sbaid.model.simulation_observer import SimulationObserver


class ProjectTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    __observer = SimulationObserver()
    __project_id = str(uuid.uuid4())
    __sim_type = SimulatorType(str(uuid.uuid4()), str(uuid.uuid4()))
    __sim_file_path =
    __project_file_path =

def test_start_simulation(self):
