import asyncio
import unittest

from gi.repository import Gio

from sbaid.model.database.global_sqlite import GlobalSQLite


class GlobalSQLiteTest(unittest.TestCase):
    async def test_create_global_sqlite(self) -> None:
        db = GlobalSQLite()
        file = Gio.File.new_for_path("/Users/fuchs/PycharmProjects/SBAid/sbaid/model/database/test.txt")


        await db.open(file)




asyncio.run(GlobalSQLiteTest().test_create_global_sqlite())