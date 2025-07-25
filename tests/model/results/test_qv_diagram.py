import unittest
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.qv_generator import QVGenerator
from tests.model.results.test_velocity_generator import VelocityGeneratorTest


class QVDiagramTest(unittest.TestCase):
    def test_qv_(self):
        test = VelocityGeneratorTest()
        qv_generator = QVGenerator()
        qv_generator.get_diagram(test.generate_random_result(), "test_id", ImageFormat.PNG)



if __name__ == '__main__':
    unittest.main()
