import unittest
from random import random

from sbaid.common.a_display import ADisplay
from sbaid.model.results.qv_generator import QVGenerator

class QVDiagramTest(unittest.TestCase):
    def test_qv_(self):
        qv_generator = QVGenerator()
        average_speed = [80, 100, 85, 40, 45]
        density = [50, 20, 50, 40, 45]
        a_displays = [ADisplay.SPEED_LIMIT_100, ADisplay.SPEED_LIMIT_120, ADisplay.SPEED_LIMIT_80,
                      ADisplay.SPEED_LIMIT_60, ADisplay.SPEED_LIMIT_60]

        qv_generator.generate_diagram(average_speed, density, a_displays)


if __name__ == '__main__':
    unittest.main()
