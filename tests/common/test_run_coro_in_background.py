import asyncio
import unittest


from sbaid import common


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__coro_finished = False

    async def my_coro(self):
        await asyncio.sleep(1)
        self.__coro_finished = True
        asyncio.get_event_loop().stop()

    def start_my_coro(self):
        common.run_coro_in_background(self.my_coro())

    async def start_my_coro_helper(self):
        self.start_my_coro()

    def test_run_coro_in_background(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.start_my_coro_helper())
        loop.run_forever()

        self.assertTrue(self.__coro_finished)


if __name__ == '__main__':
    unittest.main()
