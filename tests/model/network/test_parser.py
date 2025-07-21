"""This module contains unit tests for the cross section csv parser."""
import unittest
from sbaid.model.network.csv_cross_section_parser import CSVCrossSectionParser


class CsvParserTest(unittest.TestCase):
    """This class tests the csv parser using pythons unittest."""

    def test_file_type_guesser(self):
        parser = CSVCrossSectionParser()
        self.assertEqual(parser.can_handle_file("valid_input.csv"), True)

    def test_valid_csv(self):
        parser = CSVCrossSectionParser()

    def test_empty_csv(self):
        pass

    def test_invalid_coordinate(self):
        pass

    def test_invalid_type(self):
        pass


    def test_invalid_columns(self):
        pass

