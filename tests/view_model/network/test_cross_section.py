import unittest
import unittest.mock as mock

from sbaid.view_model.network.cross_section import CrossSection


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.__notified_name = False

    def test_property_notify(self):
        model_cs = mock.Mock()
        model_cs.id = "My Id"
        model_cs.name = "My Name"
        model_cs.hard_shoulder_available = False
        model_cs.hard_shoulder_active = False
        model_cs.b_display_active = True

        cs = CrossSection(model_cs)
        cs.connect("notify::id", self.__on_notified)
        cs.connect("notify::name", self.__on_notified)

        self.assertEqual(cs.name, "My Name")
        self.assertEqual(cs.hard_shoulder_available, False)
        self.assertEqual(cs.hard_shoulder_usable, False)
        self.assertEqual(cs.b_display_usable, True)

        cs.id = "A new id, which doesn't matter" # This shouldn't be set

        self.assertEqual(cs.id, "My Id")

        cs.name = "My New Name"
        self.assertEqual(self.__notified_name, True)
        self.assertEqual(cs.name, "My New Name")

        cs.hard_shoulder_available = True # This shouldn't be set

        self.assertEqual(cs.hard_shoulder_available, False)

        cs.b_display_usable = False

        self.assertEqual(cs.b_display_usable, False)

        cs.hard_shoulder_usable = True

        self.assertEqual(cs.hard_shoulder_usable, False)

    def __on_notified(self, cs, pspec):
        if pspec.name == "name":
            self.__notified_name = True


if __name__ == '__main__':
    unittest.main()
