import logging
import time

import grpc


logger = logging.getLogger(__name__)


class LoggingInterceptor(grpc.ServerInterceptor):

    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method

        logger.info('Receiving a request, method: `{}\''.format(method))

        start_time = time.perf_counter()
        print(start_time)
        result = continuation(handler_call_details)
        # TODO continuationの結果をまてていない、非同期にはしってるんじゃね？？？
        # https://github.com/amitsaha/python-grpc-demo/blob/d64c3179e68c69c7fd4e53ec5e7070f5a6c3c038/demo2/grpc-services/users/server/metric_interceptor.py
        # エラーハンドラも不安になってきた
        print(result)
        stop_time = time.perf_counter()
        print(stop_time)

        time_taken = stop_time - start_time

        logger.info('Run `{}\' in {:.3f}s'.format(method, time_taken))

        return result
