import colorama
import logging
import sys

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sentinelle_pb2_grpc.SentinelleStub(channel)
        result = stub.GetTestResult(sentinelle_pb2.Arguments(
            list=['application.sc_tests.views.service.api.candidates.test_is_seen_by_lapras']
            #list=['tests/test_concatenate.py'],
            #list=['polls'],
        ))
        result_color = colorama.Style.BRIGHT + (
            colorama.Fore.GREEN if result.ok else colorama.Fore.RED)
        green_face = '(*ﾟ▽ﾟ)ﾉ ﾒﾃﾞﾀｲ！！ ✨💯✨'
        red_face = '(´×ω×`) ｻﾞﾝﾈﾝ…  💦💦'

        sys.stdout.write(
            f'[{result_color}'
            f'{"OK" if result.ok else "FAIL"}{colorama.Style.RESET_ALL}]  '
            f'{green_face if result.ok else red_face}'
            f'{colorama.Style.RESET_ALL}\n\n')
        sys.stdout.write(result.content)


if __name__ == '__main__':
    colorama.init()
    logging.basicConfig()
    run()
