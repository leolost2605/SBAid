"""This module contains unittests for the Context class."""

import unittest
import uuid

from sbaid.common.simulator_type import SimulatorType


class ContextTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def test_create_project(self):
        name = str(uuid.uuid4())
        sim_type = SimulatorType(str(uuid.uuid4()), str(uuid.uuid4()))
