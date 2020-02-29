from concurrent import futures
import importlib
import logging
import sys
import unittest
from unittest.signals import _interrupt_handler

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc
from sentinelle import utils

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

    def __init__(self, inspector: InspectorProto):
        self.inspector = inspector
        # テスト実行でロードされたモジュールを覚えておきたい(エグい)
        self.initial_modules = None

    def GetTestResult(self, request, context):
        print('a')
        try:
            self._invalidate_updated_modules()
        except Exception as e:
            import traceback
            print('hoge', e)
            print(traceback.format_exc())
        print('b')

        try:
            argv = list(request.list)
            report = self.inspector.inspect(argv)

            result = sentinelle_pb2.TestResult(
                ok=report.wasPassed(),
                content=report.getContent())
        except Exception as e:
            import traceback
            print('hoge', e)
            print(traceback.format_exc())

        return result

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
                utils.deep_reload(sys.modules[m])
                # importlib.reload(sys.modules[m])


# FIXME: 限りなくシングルスレッドを期待している
# TODO: そもそも gRPC python ってデフォルトでは並列処理まわりどうなっているか調べる
# ThreadPoolExecutor かぁ
# TODO: 並列化の方針を考える(フォーク？スレッド？asyncio？？？？)

# signal only works in main threadを無視するというのはありかも？
# どうせハンドラ登録できていないわけだし…
# その場合は、teardownとか自分で呼ぶ必要がある…
#def serve(avec: InspectorProto):
def serve(avec):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        sentinelle_pb2_grpc.add_SentinelleServicer_to_server(
            Servicer(avec), server)
        server.add_insecure_port('[::]:50051')
    except Exception as e:
        import traceback
        print('hoge', e)
        print(traceback.format_exc())

    print(server.start())
    server.wait_for_termination()
