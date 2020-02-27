import logging
import sys

import grpc

from sentinelle import sentinelle_pb2
from sentinelle import sentinelle_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sentinelle_pb2_grpc.SentinelleStub(channel)
        result = stub.GetTestResult(sentinelle_pb2.Arguments(
            list=['tests/test_concatenate.py']
        ))
        green_or_red = '\033[92m' if result.ok else '\033[91m'
        close = '\033[0m'
        text = 'OK' if result.ok else 'FAIL'
        emotion = '(*ﾟ▽ﾟ)ﾉ' if result.ok else '(´×ω×`)'
        sys.stdout.write(f'[{green_or_red}{text}{close}] ... {emotion}')
        sys.stdout.write(result.content)


if __name__ == '__main__':
    logging.basicConfig()
    run()
