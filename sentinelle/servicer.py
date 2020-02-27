from concurrent import futures
import importlib
import io
import logging
import os
import sys
from unittest import TestProgram

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc

# TODO: logger!!!
# FIXME: 限りなくシングルスレッドを期待している
# TODO: そもそも gRPC python ってデフォルトでは並列処理まわりどうなっているか調べる
# TODO: 並列化の方針を考える(フォーク？スレッド？asyncio？？？？)
# TODO: github にある gRPC 公式の examples を一通り目を通す
# TODO: scouty で試す

logger = logging.getLogger(__name__)


class Servicer(sentinelle_pb2_grpc.SentinelleServicer):
    DEFAULT_ARGV = [os.path.basename(sys.executable) + " -m unittest"]

    def __init__(self, testRunnerCls):
        self.testRunnerCls = testRunnerCls
        self.program = None
        # テスト実行でロードされたモジュールを覚えておきたい(エグい)
        self.initial_modules = set()

    def GetTestResult(self, request, context):
        self._runTests(list(request.list))
        return sentinelle_pb2.TestResult(
            ok=self.program.result.wasSuccessful(),
            content=self.program.result.stream.getvalue())

    def _runTests(self, argv):
        if not self.program:
            # FIXME: エグいエグいエグいエグい
            self.initial_modules = set(sys.modules.keys())
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

    def _getTestRunnerCls(self):
        # FIXME: とりあえず結果の収集は io.StringIO 使ってごまかす
        # TODO: どっちかというと、JSON とかで結果ほしいんだよなぁ
        # FIXME: stream.close を保証できてない、リソースリークしてない？

        # コンストラクタで毎回 stream に新しい io.StringIO オブジェクトを
        # 作成するように細工してる
        class Wrapper(self.testRunnerCls):
            def __init__(self):
                super().__init__(stream=io.StringIO())
        return Wrapper

    # FIXME: 嘘しかついてない、今は全モジュール invalidate してる
    # TODO: 本当に更新されたモジュールのみを invalid するようにする
    # どうやって判断しよう？ファイルの内容からハッシュ値を得るとか？でも、各実行における
    # 差分がほしいので、ローカルに Git リポジトリを保有するとか？？
    def _invalidate_updated_modules(self):
        target_modules = set(sys.modules.keys()) - self.initial_modules
        for m in target_modules:
            if m in sys.modules:
                logger.debug(f'Invalidate {m}')
                importlib.reload(sys.modules[m])


def serve(testRunnerCls):
    """sentinelleサーバを起動する。

    `testRunnerCls` は unittest.TextTestRunner のインターフェースを持つ
    クラスを指定する(現状インスタンスはサポートしていない)
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentinelle_pb2_grpc.add_SentinelleServicer_to_server(
        Servicer(testRunnerCls), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
