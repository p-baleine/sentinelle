__all__ = [
    'SentinelleError',
    'inspectors',
    'serve',
]

import grpc

from sentinelle import inspectors
from sentinelle.servicer import serve


class SentinelleError(grpc.RpcError):
    pass
