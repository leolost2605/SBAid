import unittest

from sbaid.common.image_format import ImageFormat
from sbaid.model.results.diagram_exporter import DiagramExporter
from tests.model.results.test_velocity_generator import VelocityGeneratorTest


class DiagramExporterTest(unittest.TestCase):
    exporter = DiagramExporter()

    def test_initialize(self):
        self.assertEqual(len(self.exporter.available_diagram_types), 4)
        self.assertEqual(self.exporter.available_diagram_types[0].name, "Heatmap-Diagram")
        self.assertEqual(self.exporter.available_diagram_types[1].name, "QV-Diagram")
        self.assertEqual(self.exporter.available_diagram_types[2].name, "Display-Diagram")
        self.assertEqual(self.exporter.available_diagram_types[3].name, "Velocity-Diagram")

    def test_create_diagram(self):
        test = VelocityGeneratorTest()
        result = test.generate_random_result()

        png_qv = self.exporter.get_diagram(result, ["test_id"], ImageFormat.PNG, self.exporter.available_diagram_types[1])
        self.assertIsNotNone(png_qv)
        png_qv.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\qv.png")

        svg_qv = self.exporter.get_diagram(result, ["test_id"], ImageFormat.SVG, self.exporter.available_diagram_types[1])
        self.assertIsNotNone(svg_qv)
        svg_qv.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\qv.svg")

        png_velocity = self.exporter.get_diagram(result, ["test_id"], ImageFormat.PNG, self.exporter.available_diagram_types[3])
        self.assertIsNotNone(png_velocity)
        png_velocity.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\velocity.png")

        svg_velocity = self.exporter.get_diagram(result, ["test_id"], ImageFormat.SVG,
                                           self.exporter.available_diagram_types[3])
        self.assertIsNotNone(svg_velocity)
        svg_velocity.save_to_file(r"C:\Users\PC\Projects\SBAid\tests\model\results\generator_outputs\velocity.svg")