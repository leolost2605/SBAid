import asyncio
import random
import unittest
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.diagram_exporter import DiagramExporter
from tests.model.results.test_result_builder import ResultBuilderTest
from sbaid.model.results.result import Result

class DiagramExporterTest(unittest.TestCase):
    exporter = DiagramExporter()

    def test_initialize(self):
        self.assertEqual(len(self.exporter.available_diagram_types), 3)
        self.assertEqual(self.exporter.available_diagram_types[0].name, "Heatmap-Diagram")
        self.assertEqual(self.exporter.available_diagram_types[1].name, "QV-Diagram")
        self.assertEqual(self.exporter.available_diagram_types[2].name, "Velocity-Diagram")

    def test_create_diagram(self):
        asyncio.run(self.__test_create_diagram())

    async def __test_create_diagram(self):
        test = ResultBuilderTest()
        result = await test.generate_result(200, 10, 2)
        test_id= random.choice(list(random.choice(list(result.snapshots)).cross_section_snapshots)).cross_section_id

        png_qv = self.exporter.get_diagram(result, [test_id], ImageFormat.PNG, self.exporter.available_diagram_types[1])
        self.assertIsNotNone(png_qv)
        png_qv.save_to_file("./tests/model/results/generator_outputs/qv")

        svg_qv = self.exporter.get_diagram(result, [test_id], ImageFormat.SVG, self.exporter.available_diagram_types[1])
        self.assertIsNotNone(svg_qv)
        svg_qv.save_to_file("./tests/model/results/generator_outputs/qv")

        png_velocity = self.exporter.get_diagram(result, [test_id], ImageFormat.PNG, self.exporter.available_diagram_types[2])
        self.assertIsNotNone(png_velocity)
        png_velocity.save_to_file("./tests/model/results/generator_outputs/velocity")

        svg_velocity = self.exporter.get_diagram(result, [test_id], ImageFormat.SVG, self.exporter.available_diagram_types[2])
        self.assertIsNotNone(svg_velocity)
        svg_velocity.save_to_file("./tests/model/results/generator_outputs/velocity")

        png_heatmap = self.exporter.get_diagram(result, self.__get_result_cross_section_ids(result),
                                                 ImageFormat.PNG, self.exporter.available_diagram_types[0])
        self.assertIsNotNone(png_heatmap)
        png_velocity.save_to_file("./tests/model/results/generator_outputs/heatmap.png")

        svg_heatmap = self.exporter.get_diagram(result, self.__get_result_cross_section_ids(result),
                                                 ImageFormat.SVG, self.exporter.available_diagram_types[0])
        self.assertIsNotNone(svg_heatmap)
        svg_heatmap.save_to_file("./tests/model/results/generator_outputs/heatmap.svg")

    def __get_result_cross_section_ids(self, result: Result) -> list[str]:
        random_snapshot_cross_section_snapshots = list(random.choice(list(result.snapshots))
                                                       .cross_section_snapshots)
        cross_sections_ids: list[str] = []
        for i, snapshot in enumerate(random_snapshot_cross_section_snapshots):
            if i <= 5:
                cross_sections_ids.append(snapshot.cross_section_id)
        return cross_sections_ids