import asyncio
import unittest
from unittest import mock
from sbaid.model.results.result_manager import ResultManager as ModelResultManager
from sbaid.view_model.results.result_manager import ResultManager as ViewModelResultManager
from sbaid.view_model.results.result import Result as VMResult
from tests import result_testing_utils


class ViewModelResultTestCase(unittest.TestCase):
    __global_db = unittest.mock.AsyncMock()
    __model_result_manager = ModelResultManager(__global_db)
    __vm_result: VMResult

    def test_init(self):
        asyncio.run(self.__test_init())

    async def __test_init(self):
        result = await result_testing_utils.generate_result(20, 5, 4)
        vm_result_manager = ViewModelResultManager(self.__model_result_manager)

        await vm_result_manager.create_tag("test_tag")
        await vm_result_manager.create_tag("test_tag2")
        self.__vm_result = VMResult(result, vm_result_manager.available_tags)

    def test_diagrams(self):
        asyncio.run(self.__test_heatmap())
        asyncio.run(self.__test_velocity_diagram())
        asyncio.run(self.__test_qv_diagram())



    async def __test_heatmap(self):
        """"""
        await self.__test_init()
        self.__vm_result.diagram_types.select_item(0, True)

        # select 3 cross sections
        self.__vm_result.cross_section.select_item(3, False)
        self.__vm_result.cross_section.select_item(2, False)
        self.__vm_result.cross_section.select_item(1, False)

        self.__vm_result.formats.select_item(0, True)

        self.__vm_result.save_diagrams("./tests/model/results/generator_outputs")

        self.__vm_result.formats.select_item(1, True)
        self.__vm_result.save_diagrams("./tests/model/results/generator_outputs")

    async def __test_qv_diagram(self):
        await self.__test_init()
        self.__vm_result.diagram_types.select_item(1, True)

        # select 1 cross sections
        self.__vm_result.cross_section.select_item(3, True)

        self.__vm_result.formats.select_item(0, True)

        self.__vm_result.save_diagrams("./tests/model/results/generator_outputs")

        self.__vm_result.formats.select_item(1, True)
        self.__vm_result.save_diagrams("./tests/model/results/generator_outputs")

    async def __test_velocity_diagram(self):
        await self.__test_init()
        self.__vm_result.diagram_types.select_item(2, True)

        # select cross section
        self.__vm_result.cross_section.select_item(3, True)

        self.__vm_result.formats.select_item(0, True)

        self.__vm_result.save_diagrams("./tests/model/results/generator_outputs")

        self.__vm_result.formats.select_item(1, True)
        self.__vm_result.save_diagrams("./tests/model/results/generator_outputs")



if __name__ == '__main__':
    unittest.main()
