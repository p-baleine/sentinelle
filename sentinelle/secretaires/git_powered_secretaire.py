from sentinelle.secretaires.history import History


class GitPoweredSecretaire(object):
    def __init__(self):
        self._history = History()

    def record(self, report):
        self.history.append(
            passed=report.wasPassed(),
            content=report.getContent(),
            diff=None)

    @property
    def history(self):
        return self._history
