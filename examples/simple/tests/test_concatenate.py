import inspect
import os

from unittest import TestCase

from concatenate import concatenate


class TestConcatenate(TestCase):
    def test_concatenate(self):
        sample_file = os.path.join(os.path.dirname(__file__), "sample.exe")
        self.assertTrue(
            inspect.isgeneratorfunction(concatenate(sample_file).lines)
        )
