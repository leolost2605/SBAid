import unittest

from sbaid.common.location import Location


class LocationTestCase(unittest.TestCase):
    def test_in_between(self):
        simple_location_one = Location(1, 0)
        simple_location_two = Location(2, 0)
        simple_in_between = Location(1.5, 0)

        self.assertEqual(simple_in_between.is_between(
            simple_location_one,
            simple_location_two
        ), True)

        location_one = Location(52.03858, 4.52358)
        location_two = Location(52.18758, 6.52368)
        in_between = Location(52.11732, 5.52196)

        self.assertEqual(in_between.is_between(location_one, location_two), True)

    def test_not_in_between(self):
        location_one = Location(1, 0)
        location_two = Location(2, 0)
        location_in_between = Location(1.5, 0.1)

        self.assertEqual(location_in_between.is_between(location_one, location_two), False)


if __name__ == '__main__':
    unittest.main()
