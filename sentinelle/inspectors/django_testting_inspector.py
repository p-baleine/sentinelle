import io
from unittest.runner import TextTestResult, TextTestRunner

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from django.test.utils import (
    get_runner,
    setup_test_environment,
    teardown_test_environment)

from .inspection_report import TextInspectionReport


class DjangoTestingInspector(object):

    def __init__(self, testRunnerCls=TextTestRunner, **kwargs):
        self.testRunnerCls = testRunnerCls

        django.setup()

        # TODO: Runner にコマンドライン引数のオプションを渡してあげる
        if not settings.TEST_RUNNER or \
           settings.TEST_RUNNER == 'django.test.runner.DiscoverRunner':
            self.program = TameDiscoverRunner(**kwargs)
        else:
            self.program = get_runner(settings)(**kwargs)

    def inspect(self, argv):
        runner = _getTestRunnerClass(self.testRunnerCls)()

        # HACK: self.program(django.test.runner.DiscoverRunner) の
        # test_runner フィールドを runner を返すクロージャで上書きすることで
        # runner 経由でテスト結果を受け取れるようにする
        self.program.test_runner = lambda **kwargs: runner

        failures = self.program.run_tests(argv)

        # (少なくとも DiscoverRunner は)TestResult にアクセスさせてくれない
        # ので、ダミーの TestResult を作る
        result = PseudoTextTestResult(stream=runner.stream, failures=failures)

        self.report = TextInspectionReport(result)

        return self.report


class TameDiscoverRunner(DiscoverRunner):
    """Dedicated thread で実行される想定の DiscoverRunner

    DiscoverRunner との違いはシグナルの登録を行わない点のみ。
    """

    # Overrides DiscoverRunner
    def setup_test_environment(self, **kwargs):
        setup_test_environment(debug=self.debug_mode)

    # Overrides DiscoverRunner
    def teardown_test_environment(self, **kwargs):
        teardown_test_environment()


class PseudoTextTestResult(TextTestResult):

    def __init__(self, failures, **kwargs):
        super().__init__(descriptions=True, verbosity=1, **kwargs)
        # テストの結果、 wasSuccessful() は failures のリストの流さで
        # 判断されるので、テストに失敗しているときは適当なリストを入れておく
        self.failures = [1 for _ in range(failures)]


def _getTestRunnerClass(testRunnerCls):
    class Wrapper(testRunnerCls):
        def __init__(self, **kwargs):
            super().__init__(stream=io.StringIO(), **kwargs)
    return Wrapper
