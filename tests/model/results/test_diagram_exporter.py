import unittest

from sbaid.model.results.diagram_exporter import DiagramExporter


class DiagramExporterTest(unittest.TestCase):

    def test_init(self):
        exporter = DiagramExporter()
