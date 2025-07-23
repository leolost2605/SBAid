import unittest
from random import random

from sbaid.model.results.qv_generator import QVGenerator

class QVDiagramTest(unittest.TestCase):
    def test_qv_(self):
        qv_generator = QVGenerator()
        average_speed = list[int]
        density = list[int]

        data = tuple[average_speed, density]
        qv_generator.generate_diagram(data)


if __name__ == '__main__':
    unittest.main()
