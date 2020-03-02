# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sentinelle/sentinelle.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='sentinelle/sentinelle.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x1bsentinelle/sentinelle.proto\"\x19\n\tArguments\x12\x0c\n\x04list\x18\x01 \x03(\t\"\xa3\x01\n\nTestResult\x12\n\n\x02ok\x18\x01 \x02(\x08\x12\x0f\n\x07\x63ontent\x18\x02 \x02(\t\x12$\n\x04\x64iff\x18\x03 \x02(\x0b\x32\x16.TestResult.Difference\x1aR\n\nDifference\x12\x0e\n\x06\x63ommit\x18\x01 \x02(\t\x12\x10\n\x08previous\x18\x02 \x02(\t\x12\x15\n\rchanged_files\x18\x03 \x03(\t\x12\x0b\n\x03raw\x18\x04 \x02(\t21\n\nSentinelle\x12#\n\x06\x44oTest\x12\n.Arguments\x1a\x0b.TestResult\"\x00'
)




_ARGUMENTS = _descriptor.Descriptor(
  name='Arguments',
  full_name='Arguments',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='list', full_name='Arguments.list', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=31,
  serialized_end=56,
)


_TESTRESULT_DIFFERENCE = _descriptor.Descriptor(
  name='Difference',
  full_name='TestResult.Difference',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='commit', full_name='TestResult.Difference.commit', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='previous', full_name='TestResult.Difference.previous', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='changed_files', full_name='TestResult.Difference.changed_files', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='raw', full_name='TestResult.Difference.raw', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=140,
  serialized_end=222,
)

_TESTRESULT = _descriptor.Descriptor(
  name='TestResult',
  full_name='TestResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ok', full_name='TestResult.ok', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='TestResult.content', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='diff', full_name='TestResult.diff', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_TESTRESULT_DIFFERENCE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=222,
)

_TESTRESULT_DIFFERENCE.containing_type = _TESTRESULT
_TESTRESULT.fields_by_name['diff'].message_type = _TESTRESULT_DIFFERENCE
DESCRIPTOR.message_types_by_name['Arguments'] = _ARGUMENTS
DESCRIPTOR.message_types_by_name['TestResult'] = _TESTRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Arguments = _reflection.GeneratedProtocolMessageType('Arguments', (_message.Message,), {
  'DESCRIPTOR' : _ARGUMENTS,
  '__module__' : 'sentinelle.sentinelle_pb2'
  # @@protoc_insertion_point(class_scope:Arguments)
  })
_sym_db.RegisterMessage(Arguments)

TestResult = _reflection.GeneratedProtocolMessageType('TestResult', (_message.Message,), {

  'Difference' : _reflection.GeneratedProtocolMessageType('Difference', (_message.Message,), {
    'DESCRIPTOR' : _TESTRESULT_DIFFERENCE,
    '__module__' : 'sentinelle.sentinelle_pb2'
    # @@protoc_insertion_point(class_scope:TestResult.Difference)
    })
  ,
  'DESCRIPTOR' : _TESTRESULT,
  '__module__' : 'sentinelle.sentinelle_pb2'
  # @@protoc_insertion_point(class_scope:TestResult)
  })
_sym_db.RegisterMessage(TestResult)
_sym_db.RegisterMessage(TestResult.Difference)



_SENTINELLE = _descriptor.ServiceDescriptor(
  name='Sentinelle',
  full_name='Sentinelle',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=224,
  serialized_end=273,
  methods=[
  _descriptor.MethodDescriptor(
    name='DoTest',
    full_name='Sentinelle.DoTest',
    index=0,
    containing_service=None,
    input_type=_ARGUMENTS,
    output_type=_TESTRESULT,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SENTINELLE)

DESCRIPTOR.services_by_name['Sentinelle'] = _SENTINELLE

# @@protoc_insertion_point(module_scope)
