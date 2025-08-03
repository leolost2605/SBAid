"""This module contains unit tests for the result diagrams."""
import unittest
import asyncio
from sbaid.model.results.result import Result
from sbaid.model.results.heatmap_generator import HeatmapGenerator
from sbaid.common.image_format import ImageFormat
from tests.model.results.test_result_builder import ResultBuilderTest
import random


class DiagramTest(unittest.TestCase):
    """This class tests the generating of result diagrams."""

    def test_random_data_heatmap(self):
        asyncio.run(self._test_random_data_heatmap())

    async def _test_random_data_heatmap(self):
        generator = HeatmapGenerator()
        test = ResultBuilderTest()
        result = await test.generate_result(50, 10, 4)
        cross_section_ids = self.__get_result_cross_section_ids(result)
        png_image = generator.get_diagram(result, cross_section_ids, ImageFormat.PNG)
        png_image.save_to_file(r"C:\Users\mleom\PycharmProjects\SBAid\tests\model\results\generator_outputs\heatmap.png")

        svg_image = generator.get_diagram(result, cross_section_ids, ImageFormat.SVG)
        svg_image.save_to_file(r"C:\Users\mleom\PycharmProjects\SBAid\tests\model\results\generator_outputs\heatmap.svg")

    def __get_result_cross_section_ids(self, result: Result) -> list[str]:
        random_snapshot_cross_section_snapshots = list(random.choice(list(result.snapshots))
                                                       .cross_section_snapshots)
        cross_sections_ids: list[str] = []
        for i, snapshot in enumerate(random_snapshot_cross_section_snapshots):
            if i <= 5:
                cross_sections_ids.append(snapshot.cross_section_id)
        return cross_sections_ids