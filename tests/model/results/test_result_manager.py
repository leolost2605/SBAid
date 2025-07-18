import unittest
from sbaid.model.results.result_manager import ResultManager
from sbaid.common.tag import Tag
class ResultManagerTest(unittest.TestCase):

    def test_add_tag(self):
        result_manager = ResultManager
        new_tag = Tag("random", "hi")
        result_manager.create_tag(new_tag)
        self.assertEqual(new_tag.tag_id, "random")


