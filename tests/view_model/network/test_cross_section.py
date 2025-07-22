import unittest
import unittest.mock as mock

from sbaid.view_model.network.cross_section import CrossSection


class MyTestCase(unittest.TestCase):
    def test_property_notify(self):
        model_cs = mock.Mock()
        model_cs.id = "My Id"

        cs = CrossSection(model_cs)

        cs.id = "A new id, which doesn't matter" # This shouldn't be set

        self.assertEqual(cs.id, "My Id")


if __name__ == '__main__':
    unittest.main()
