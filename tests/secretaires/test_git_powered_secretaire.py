import io
import unittest
from unittest.runner import TextTestResult

from sentinelle.inspectors.inspection_report import TextInspectionReport
from sentinelle.secretaires import History, GitPoweredSecretaire


class GitPoweredSecretaierTest(unittest.TestCase):

    def test_record(self):
        secretaire = GitPoweredSecretaire()
        stream = io.StringIO()
        stream.write("present time!")
        report = TextInspectionReport(TextTestResult(
            stream=stream,
            descriptions="",
            verbosity=1,
        ))
        previous_history_count = len(secretaire.history)

        secretaire.record(report)

        self.assertEqual(previous_history_count + 1, len(secretaire.history))
        self.assertEqual("present time!", secretaire.history.latest.content)

    def test_history(self):
        secretaire = GitPoweredSecretaire()
        self.assertIsInstance(secretaire.history, History)
