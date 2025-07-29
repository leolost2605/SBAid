import unittest

from gi.repository import Gio
from gi.repository import GObject

from sbaid import common


class IntObject(GObject.GObject):
    value: int

    def __init__(self, val: int):
        super().__init__()
        self.value = val


class ListModelIteratorTestCase(unittest.TestCase):
    def test_iterator(self):
        model = Gio.ListStore.new(IntObject)
        model.append(IntObject(0))
        model.append(IntObject(1))
        model.append(IntObject(2))
        model.append(IntObject(3))

        for i, x in enumerate(common.list_model_iterator(model)):
            self.assertEqual(i, x.value)


if __name__ == '__main__':
    unittest.main()
