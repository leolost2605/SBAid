import unittest
from unittest import mock
from sbaid.common.tag import Tag
from sbaid.model.results.result_manager import ResultManager as ModelResultManager
from sbaid.view_model.results.result_manager import ResultManager as ViewResultManager
from tests import result_testing_utils

class ViewModelResultManagerTest(unittest.IsolatedAsyncioTestCase):
    __global_db = unittest.mock.AsyncMock()
    __model_result_manager = ModelResultManager(__global_db)

    async def test_delete_result(self):
        # construct model result manager with one random result
        result = await result_testing_utils.generate_result(1, 5, 4)
        await self.__model_result_manager.register_result(result)

        # assert added successfully
        self.assertIn(result, self.__model_result_manager.results)

        # construct view model result manager
        vm_manager = ViewResultManager(self.__model_result_manager)
        self.assertEqual(vm_manager.results.get_n_items(), 1)

        # delete result
        await vm_manager.delete_result(result.id)

        # assert deleted
        self.assertNotIn(result, self.__model_result_manager.results)
        self.assertEqual(vm_manager.results.get_n_items(), 0)

    async def test_add_remove_tags(self):
        # construct view model result manager
        vm_manager = ViewResultManager(self.__model_result_manager)
        pos = await vm_manager.create_tag("testing")

        tag = vm_manager.available_tags.get_item(pos)

        self.assertIsInstance(tag, Tag)
        self.assertEqual(tag.name, "testing")
        self.assertIn(tag, self.__model_result_manager.available_tags)

        await vm_manager.delete_tag(tag.tag_id)
        self.assertNotIn(tag, self.__model_result_manager.available_tags)
        self.assertNotIn(tag, vm_manager.available_tags)

if __name__ == '__main__':
    unittest.main()
