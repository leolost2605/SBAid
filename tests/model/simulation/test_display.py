"""This module contains unittests for the Display class."""

import unittest

from sbaid.common.a_display import ADisplay
from sbaid.common.b_display import BDisplay
from sbaid.model.simulation.display import Display


class DisplayTestCase(unittest.TestCase):
    """This class tests the display using pythons unittest."""

    def test_empty_display(self):
        """Test an empty display, getters returning None."""
        display = Display()
        self.assertIsNone(display.get_a_display("my_cross_section", 0))
        self.assertIsNone(display.get_b_display("my_cross_section"))

    def test_add_displays(self):
        """Test adding display."""
        display = Display()

        display.set_a_display("my_cross_section", 0, ADisplay.SPEED_LIMIT_LIFTED)
        display.set_b_display("my_cross_section", BDisplay.OFF)
        self.assertEqual(display.get_a_display("my_cross_section", 0),
                          ADisplay.SPEED_LIMIT_LIFTED)
        self.assertEqual(display.get_b_display("my_cross_section"), BDisplay.OFF)

    def test_update_display(self):
        """Test updating display. New values are updated."""
        display = Display()
        display.set_a_display("my_cross_section", 0, ADisplay.SPEED_LIMIT_LIFTED)
        display.set_b_display("my_cross_section", BDisplay.OFF)

        self.assertEqual(display.get_a_display("my_cross_section", 0), ADisplay.SPEED_LIMIT_LIFTED)
        self.assertEqual(display.get_b_display("my_cross_section"), BDisplay.OFF)

        display.set_a_display("my_cross_section", 0, ADisplay.SPEED_LIMIT_100)
        display.set_b_display("my_cross_section", BDisplay.TRAFFIC_JAM)

        self.assertEqual(display.get_a_display("my_cross_section", 0), ADisplay.SPEED_LIMIT_100)
        self.assertEqual(display.get_b_display("my_cross_section"), BDisplay.TRAFFIC_JAM)

    def test_multiple_lanes(self):
        """Test adding display with multiple a displays per cross-section."""
        display = Display()
        display.set_a_display("my_cross_section", 0, ADisplay.SPEED_LIMIT_110)
        display.set_a_display("my_cross_section", 1, ADisplay.SPEED_LIMIT_130)
        display.set_b_display("my_cross_section", BDisplay.OFF)

        self.assertEqual(display.get_a_display("my_cross_section", 0), ADisplay.SPEED_LIMIT_110)
        self.assertEqual(display.get_a_display("my_cross_section", 1), ADisplay.SPEED_LIMIT_130)
        self.assertEqual(display.get_b_display("my_cross_section"), BDisplay.OFF)
