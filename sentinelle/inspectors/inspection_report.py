from unittest.result import TestResult
from unittest.runner import TextTestResult

try:
    from typing import Protocol
except Exception:
    from typing_extensions import Protocol


class InspectionReportProto(Protocol):

    def wasPassed(self, test_result: TestResult) -> bool:
        pass

    def getContent(self) -> str:
        pass


class TextInspectionReport(object):

    def __init__(self, test_result: TextTestResult):
        self.test_result = test_result

    def wasPassed(self) -> bool:
        return self.test_result.wasSuccessful()

    def getContent(self) -> str:
        return self.test_result.stream.getvalue()
