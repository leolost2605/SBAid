import asyncio
import unittest

from gi.repository import Gio
from gi.events import GLibEventLoopPolicy

from sbaid import common


class MakeDirTestCase(unittest.TestCase):
    def test_make_dir_with_parents_async(self):
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        loop = asyncio.get_event_loop()
        task = loop.create_task(self._test_make_dir_with_parents_async())
        loop.run_until_complete(task)

    async def _test_make_dir_with_parents_async(self):
        path = "./FirstDirectory/SecondDirectory/ThirdDirectory"
        file = Gio.File.new_for_path(path)
        await common.make_directory_with_parents_async(file)

        assert file.query_exists()


if __name__ == '__main__':
    unittest.main()
