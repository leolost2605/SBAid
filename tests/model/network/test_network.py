import unittest
from sbaid.model.network.parser_factory import ParserFactory


class NetworkTest(unittest.TestCase):

    def test_factory_singleton(self):
        first_instance = ParserFactory()
        second_instance = ParserFactory()
        self.assertEqual(first_instance, second_instance)
