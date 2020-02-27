from unittest import TestProgram


def create_server(runner):
    return Server(runner=runner)


class Server(object):
    # dummy??

    def __init__(self, runner):
        self.runner = runner
        self.program = None

    def start(self):
        # on every request...
        # argv may be passed from client...
        #argv = ['python!', 'tests.test_concatenate']
        # 当たり前だけど、examples/simpleでたたかないと動かない
        argv = ['python!', 'tests/test_concatenate.py']
        program = TestProgram(
            module=None,
            testRunner=self.runner, exit=False, argv=argv)
        print('hoge', program.test)
        print(program.result)
