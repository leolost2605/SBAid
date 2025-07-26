import unittest
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.qv_generator import QVGenerator
from tests.model.results.test_velocity_generator import VelocityGeneratorTest


class QVDiagramTest(unittest.TestCase):
    generator = QVGenerator()
        # todo maybe make all diagram tests one class
    def test_qv_(self):
        test = VelocityGeneratorTest()
        result = test.generate_random_result()

        png_image = self.generator.get_diagram(result, "test_id", ImageFormat.PNG)
        png_image.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\diagram.png")

        svg_image = self.generator.get_diagram(result, "test_id", ImageFormat.SVG)
        svg_image.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\diagram.svg")
