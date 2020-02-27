import inspect
import os

from unittest import TestCase

from concatenate import concatenate


class TestConcatenate(TestCase):
    def test_concatenate(self):
        sample_file = os.path.join(os.path.dirname(__file__), "sample.txt")
        self.assertTrue(
            inspect.isgeneratorfunction(concatenate(sample_file).lines)
        )

    # def test_fail(self):
    #     self.assertEqual("玲音", "レイン")

    def test_success(self):
        self.assertTrue("ぷれぜんとでい、ぷれぜんとたいむ")
