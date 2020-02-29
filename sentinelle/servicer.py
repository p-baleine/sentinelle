from concurrent import futures
import logging
import sys
import time

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc
from sentinelle import utils
from sentinelle.inspectors import InspectorProto
from sentinelle import interceptors

# TODO: logger!!!

# NOTE: 実行履歴を持ちたい
# 実行履歴が鍵になる気がしている。
# + 今回実行すべきテスト対象 :: 前回から今回で差分のあったファイルの影響範囲
# + テスト落ちたときに知りたいこと :: green から red になったタイミングのファイルの変更範囲

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


# FIXME: 限りなくシングルスレッドを期待している
def serve(avec: InspectorProto):
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[interceptors.GlobalExceptionInterceptor()])
    sentinelle_pb2_grpc.add_SentinelleServicer_to_server(
        Servicer(avec), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        server.wait_for_termination()
    except AttributeError as e:
        if str(e) == ('\'_Server\' object has no attribute'
                      ' \'wait_for_termination\''):
            # https://github.com/grpc/grpc/blob/5b9b5ebe26b3c84477d989fbcda5959e9ec00adf/examples/python/data_transmission/server.py#L105
            try:
                while 1:
                    time.sleep(10)
            except KeyboardInterrupt:
                server.stop(0)
        else:
            raise e
