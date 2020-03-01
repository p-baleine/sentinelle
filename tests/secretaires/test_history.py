import unittest

from sentinelle.secretaires.history import History
from sentinelle.secretaires.history import HistoryEvent


class HistoryTest(unittest.TestCase):

    def test_latest(self):
        history = History()
        history.append(True, "abcdef", None)
        self.assertEqual("abcdef", history.latest.content)

    def test_append(self):
        history = History()
        history.append(True, "", None)
        self.assertEqual(1, len(history))

    def test_length(self):
        history = History()
        history.append(True, "", None)
        history.append(True, "", None)
        history.append(True, "", None)
        self.assertEqual(3, len(history))


class HistoryEventTest(unittest.TestCase):

    @unittest.skip('diffの詳細がまだわからん')
    def test_diff(self):
        pass

    def test_wasSuccessful(self):
        event = HistoryEvent(
            passed=False, content="present days", diff=None)
        self.assertFalse(event.passed)

    def test_content(self):
        event = HistoryEvent(
            passed=False, content="present days", diff=None)
        self.assertEqual("present days", event.content)
