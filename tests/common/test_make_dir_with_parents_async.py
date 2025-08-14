import unittest

from gi.repository import Gio

from sbaid import common


class MakeDirTestCase(unittest.IsolatedAsyncioTestCase):
    @unittest.skip("TODO: doesn't work in test runner")
    async def test_make_dir_with_parents_async(self):
        path = "./FirstDirectory/SecondDirectory/ThirdDirectory"
        file = Gio.File.new_for_path(path)
        await common.make_directory_with_parents_async(file)

        assert file.query_exists()


if __name__ == '__main__':
    unittest.main()
