# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from sentinelle import sentinelle_pb2 as sentinelle_dot_sentinelle__pb2


class SentinelleStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetTestResult = channel.unary_unary(
        '/Sentinelle/GetTestResult',
        request_serializer=sentinelle_dot_sentinelle__pb2.Arguments.SerializeToString,
        response_deserializer=sentinelle_dot_sentinelle__pb2.TestResult.FromString,
        )


class SentinelleServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetTestResult(self, request, context):
    """Obtains the results of running tests specified in `Arguments`.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SentinelleServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetTestResult': grpc.unary_unary_rpc_method_handler(
          servicer.GetTestResult,
          request_deserializer=sentinelle_dot_sentinelle__pb2.Arguments.FromString,
          response_serializer=sentinelle_dot_sentinelle__pb2.TestResult.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Sentinelle', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))