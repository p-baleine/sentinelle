from typing import List

try:
    from typing import Protocol
except Exception:
    from typing_extensions import Protocol

from .inspection_report import InspectionReport


class InspectorProto(Protocol):
    def inpect(self, argv: List[str]) -> InspectionReport:
        pass
