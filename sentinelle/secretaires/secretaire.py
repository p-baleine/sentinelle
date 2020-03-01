from typing import NoReturn

try:
    from typing import Protocol
except Exception:
    from typing_extensions import Protocol

from sentinelle.inspectors import InspectionReportProto
from sentinelle.secretaires import History


class SecretaireProto(Protocol):

    def record(self, report: InspectionReportProto) -> NoReturn:
        pass

    def history(self) -> History:
        pass
