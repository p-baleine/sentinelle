class Concatenator(object):
    def __init__(self, files):
        self._files = files

    def lines(self):
        for file in self.files:
            with open(file, 'rt') as f:
                line = f.readline()
                while line:
                    yield line
                    line = f.readline()

    @property
    def files(self):
        return self._files


def concatenate(files):
    return Concatenator(files)
