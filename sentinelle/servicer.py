from concurrent import futures
import importlib
import logging
import os
import sys

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc
from sentinelle.inspectors import InspectorProto

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

    def __init__(self, inspector):
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
    # どうやって判断しよう？ファイルの内容からハッシュ値を得るとか？でも、各実行における
    # 差分がほしいので、ローカルに Git リポジトリを保有するとか？？
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
                importlib.reload(sys.modules[m])


# FIXME: 限りなくシングルスレッドを期待している
# TODO: そもそも gRPC python ってデフォルトでは並列処理まわりどうなっているか調べる
# ThreadPoolExecutor かぁ
# TODO: 並列化の方針を考える(フォーク？スレッド？asyncio？？？？)
def serve(avec: InspectorProto):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentinelle_pb2_grpc.add_SentinelleServicer_to_server(
        Servicer(avec), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
