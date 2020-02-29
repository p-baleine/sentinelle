import logging

import grpc

import sentinelle

logger = logging.getLogger(__name__)


class GlobalExceptionInterceptor(grpc.ServerInterceptor):
    """グローバルなエラーハンドラ
    """

    def intercept_service(self, continuation, handler_call_details):
        try:
            return continuation(handler_call_details)
        except sentinelle.SentinelleError as e:
            logger.error(e)
            raise e
