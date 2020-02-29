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

    def __init__(self, testRunnerCls=TextTestRunner):
        self.testRunnerCls = testRunnerCls
        django.setup()

        # TODO: Runner にコマンドライン引数のオプションを渡してあげる
        if settings.TEST_RUNNER and \
           settings.TEST_RUNNER != 'django.test.runner.DiscoverRunner':
            self.program = get_runner(settings)()
        else:
            self.program = TameDiscoverRunner(keepdb=True)

    def inspect(self, argv):
        runner = _getTestRunnerClass(self.testRunnerCls)()

        # HACK: self.program(django.test.runner.DiscoverRunner) の
        # test_runner フィールドを以下で上書きすることで、runner 経由で
        # テスト結果を受け取れるようにする
        self.program.test_runner = lambda **kwargs: runner

        try:
            print('1')
            failures = self.program.run_tests(argv)
            print('2')
        except Exception as e:
            import traceback
            print('hoge', e)
            print(traceback.format_exc())

        print('3')
        result = TextTestResult(
            stream=runner.stream, descriptions=True, verbosity=1)
        print('4')
        if failures:
            result.failures = ['hoge' for _ in range(failures)]

        print('6')
        self.report = TextInspectionReport(result)
        print('7')

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


def _getTestRunnerClass(testRunnerCls):
    class Wrapper(testRunnerCls):
        def __init__(self):
            super().__init__(stream=io.StringIO())
    return Wrapper
