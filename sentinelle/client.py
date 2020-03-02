import colorama
import logging
import os
import sys
import time

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        green_face = '(*ﾟ▽ﾟ)ﾉ ﾒﾃﾞﾀｲ！！ ✨💯✨'
        red_face = 'ヾ(´༎ຶ╻༎ຶ)ﾉﾞ ｻﾞﾝﾈﾝ…  💦💦'
        waiting_gace = '(・∀・) ﾁｮｯﾄﾏｯﾃﾈ…\n'

        while True:
            os.system('tput reset')
            sys.stdout.write('[…]  ' + waiting_gace)
            sys.stdout.flush()

            stub = sentinelle_pb2_grpc.SentinelleStub(channel)
            result = stub.DoTest(sentinelle_pb2.Arguments(
                list=['application.sc_tests.views.service.api.candidates.test_is_seen_by_lapras']
                #list=['tests/test_concatenate.py'],
                #list=['polls'],
            ))
            result_color = colorama.Style.BRIGHT + (
                colorama.Fore.GREEN if result.ok else colorama.Fore.RED)

            os.system('tput reset')
            sys.stdout.write(
                f'[{result_color}'
                f'{"OK" if result.ok else "FAIL"}{colorama.Style.RESET_ALL}]  '
                f'{green_face if result.ok else red_face}'
                f'{colorama.Style.RESET_ALL}\n\n')
            sys.stdout.write(result.content)

            if not result.ok:
                sys.stdout.write('\n\n' + result.diff.raw)

            sys.stdout.flush()

            time.sleep(15)


if __name__ == '__main__':
    colorama.init()
    logging.basicConfig()
    run()
