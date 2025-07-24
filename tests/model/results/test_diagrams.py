"""This module contains unit tests for the result diagrams."""
import unittest
from sbaid.model.results.heatmap_generator import HeatmapGenerator
import random
from gi.repository import GLib


class DiagramTest(unittest.TestCase):
    """This class tests the generating of result diagrams."""
    def test_random_data_heatmap(self):
        generator = HeatmapGenerator()
        diagram_data = []
        for i in range(200):
            row = []
            for j in range(20):
                a = random.uniform(0, 140)
                row.append(a)
            diagram_data.append(row)
        cross_sections = []
        for i in range(20):
            cross_sections.append("MQ%d"%i)
        timestamps = []
        for i in range(200):
            if i%50 == 0:
                timestamps.append("time: %d" % i)
            else:
                timestamps.append("")

        date = GLib.DateTime.new_utc(2025, 7, 22, 13, 16, 45)
        generator.get_diagram("result_name", "project_name",
                                   diagram_data, cross_sections, timestamps, date)
