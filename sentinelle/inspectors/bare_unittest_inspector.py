import io
import os
import sys
from unittest import TestProgram, TextTestRunner

from .inspection_report import TextInspectionReport


class BareUnittestInspector(object):
    DEFAULT_ARGV = [os.path.basename(sys.executable) + " -m unittest"]

    def __init__(self, testRunnerCls=TextTestRunner):
        self.program = None
        self.testRunnerCls = testRunnerCls
        self.report = None

    def inspect(self, argv):
        if not self.program:
            # TestProgram は生成時に runTests() を実行しているため
            # 初回は runTests() は呼ばなくてよい
            self.program = TestProgram(
                module=None,
                testRunner=self._getTestRunnerCls(),
                exit=False,
                argv=self.DEFAULT_ARGV + argv)
        else:
            self.program.parseArgs(self.DEFAULT_ARGV + argv)
            self.program.runTests()

        self.report = TextInspectionReport(self.program.result)

        return self.report

    def _getTestRunnerCls(self):
        # TODO: 結果は文字列じゃなくて JSON で返却したい
        # FIXME: stream.close を保証できてない、リソースリークしてない？

        # コンストラクタで毎回 stream に新しい io.StringIO オブジェクトを
        # 作成するように細工してる
        class Wrapper(self.testRunnerCls):
            def __init__(self):

                super().__init__(stream=io.StringIO())
        return Wrapper
