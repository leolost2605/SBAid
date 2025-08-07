import asyncio
import unittest
from unittest import mock
from sbaid.model.results.result_manager import ResultManager as ModelResultManager
from sbaid.view_model.results.result_manager import ResultManager as ViewModelResultManager
from tests.model.results.test_result_builder import ResultBuilderTest
from sbaid.view_model.results.result import Result as VMResult


class ViewModelResultTestCase(unittest.TestCase):
    __global_db = unittest.mock.AsyncMock()
    __model_result_manager = ModelResultManager(__global_db)

    def test_init(self):
        asyncio.run(self.__test_init())

    async def __test_init(self):
        result = await ResultBuilderTest().generate_result(20, 5, 4)
        vm_result_manager = ViewModelResultManager(self.__model_result_manager)

        await vm_result_manager.create_tag("test_tag")
        await vm_result_manager.create_tag("test_tag2")
        vm_result = VMResult(result, vm_result_manager.available_tags)

        vm_result.cross_section.select_item(3, False)
        vm_result.cross_section.select_item(2, False)
        vm_result.cross_section.select_item(1, False)

        vm_result.diagram_types.select_item(0, True)
        vm_result.formats.select_item(0, True)

        vm_result.load_previews()
        vm_result.save_diagrams(r"C:\Users\PC\Desktop\python_testing_locally")



if __name__ == '__main__':
    unittest.main()
