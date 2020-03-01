from typing import List

try:
    from typing import Protocol
except Exception:
    from typing_extensions import Protocol

from sentinelle.inspectors import InspectionReportProto


class InspectorProto(Protocol):
    def inpect(self, argv: List[str]) -> InspectionReportProto:
        pass
