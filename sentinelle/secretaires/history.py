from collections import namedtuple
from typing import NoReturn

try:
    from typing import Protocol
except Exception:
    from typing_extensions import Protocol


class Difference(Protocol):
    pass


HistoryEvent = namedtuple('HistoryEvent', [
    'passed',
    'content',
    'diff'])


class History(object):

    def __init__(self):
        self._data = []

    @property
    def latest(self) -> HistoryEvent:
        return self._data[0]

    def append(
        self,
        passed: bool,
        content: str,
        diff: Difference
    ) -> NoReturn:
        self._data.append(HistoryEvent(
            passed=passed,
            content=content,
            diff=diff))

    def __len__(self):
        return len(self._data)

    def __getitem__(self, event):
        return self._data[event]
