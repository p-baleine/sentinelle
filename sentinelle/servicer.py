from concurrent import futures
import logging
import sys

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc
from sentinelle import utils
from sentinelle.inspectors import InspectorProto
from sentinelle import interceptors

# TODO: logger!!!
# TODO: github にある gRPC 公式の examples を一通り目を通す
# TODO: scouty で試す

# NOTE: 実行履歴を持ちたい
# 実行履歴が鍵になる気がしている。
# + 今回実行すべきテスト対象 :: 前回から今回で差分のあったファイルの影響範囲
# + テスト落ちたときに知りたいこと :: green から red になったタイミングのファイルの変更範囲
# などなど。「実行履歴」じゃなくて、sentinelle っぽい名前が良いなぁ。
# 全体的に servicer からロジックを切り出して、sentinelle っぽくしたい(楽しそう)

logger = logging.getLogger(__name__)


class Servicer(sentinelle_pb2_grpc.SentinelleServicer):

    def __init__(self, inspector: InspectorProto):
        self.inspector = inspector
        # テスト実行でロードされたモジュールを覚えておきたい(エグい)
        self.initial_modules = None

    def GetTestResult(self, request, context):
        self._invalidate_updated_modules()

        argv = list(request.list)
        report = self.inspector.inspect(argv)

        return sentinelle_pb2.TestResult(
            ok=report.wasPassed(),
            content=report.getContent())

    # FIXME: 嘘しかついてない、今は全モジュール invalidate してる
    # TODO: 本当に更新されたモジュールのみを invalid するようにする
    def _invalidate_updated_modules(self):
        if not self.initial_modules:
            # 初回は(テスト対象及びテストモジュールを読み込む前にこのメソッドを
            # 実行するので)テスト対象及びテストモジュール以外のモジュールを記憶
            # する。FIXME: 刳い
            self.initial_modules = set(sys.modules.keys())
            return

        target_modules = set(sys.modules.keys()) - self.initial_modules

        for m in target_modules:
            if m in sys.modules:
                logger.debug(f'Invalidate {m}')
                utils.deep_reload(sys.modules[m])
                # importlib.reload(sys.modules[m])


# FIXME: 限りなくシングルスレッドを期待している
# TODO: そもそも gRPC python ってデフォルトでは並列処理まわりどうなっているか調べる
# ThreadPoolExecutor かぁ
def serve(avec: InspectorProto):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[interceptors.GlobalExceptionInterceptor()])
    sentinelle_pb2_grpc.add_SentinelleServicer_to_server(
        Servicer(avec), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # TODO: wait_for_termination は experimental で古いバージョンだと存在しないため
    # バージョン毎に切り分けする
    # https://github.com/grpc/grpc/blob/8aff9ec59220d3394d36c1e43c1a5fbb3c2e9574/src/python/grpcio/grpc/__init__.py#L1456
    server.wait_for_termination()
