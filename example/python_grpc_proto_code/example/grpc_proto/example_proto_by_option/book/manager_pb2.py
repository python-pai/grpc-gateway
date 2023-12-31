# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example/grpc_proto/example_proto_by_option/book/manager.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from example.python_grpc_proto_code.example.grpc_proto.example_proto_by_option.common import p2p_validate_pb2 as example_dot_grpc__proto_dot_example__proto__by__option_dot_common_dot_p2p__validate__pb2
from example.python_grpc_proto_code.example.grpc_proto.example_proto_by_option.common import api_pb2 as example_dot_grpc__proto_dot_example__proto__by__option_dot_common_dot_api__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n=example/grpc_proto/example_proto_by_option/book/manager.proto\x12\x16\x62ook_manager_by_option\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x44\x65xample/grpc_proto/example_proto_by_option/common/p2p_validate.proto\x1a;example/grpc_proto/example_proto_by_option/common/api.proto\"n\n\x11\x43reateBookRequest\x12\x0c\n\x04isbn\x18\x01 \x01(\t\x12\x11\n\tbook_name\x18\x02 \x01(\t\x12\x13\n\x0b\x62ook_author\x18\x03 \x01(\t\x12\x11\n\tbook_desc\x18\x04 \x01(\t\x12\x10\n\x08\x62ook_url\x18\x05 \x01(\t\"!\n\x11\x44\x65leteBookRequest\x12\x0c\n\x04isbn\x18\x01 \x01(\t\"p\n\x0eGetBookRequest\x12.\n\x04isbn\x18\x01 \x01(\tB \x8a\x43\x1dr\x1b\x82\x02\x18grpc-gateway@field|Query\x12\x16\n\x0enot_use_field1\x18\x02 \x01(\t\x12\x16\n\x0enot_use_field2\x18\x03 \x01(\t\"\xcc\x01\n\rGetBookResult\x12\x0c\n\x04isbn\x18\x01 \x01(\t\x12\x11\n\tbook_name\x18\x02 \x01(\t\x12\x13\n\x0b\x62ook_author\x18\x03 \x01(\t\x12\x11\n\tbook_desc\x18\x04 \x01(\t\x12\x10\n\x08\x62ook_url\x18\x05 \x01(\t\x12/\n\x0b\x63reate_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bupdate_time\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"s\n\x12GetBookListRequest\x12\x39\n\x10next_create_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00\x88\x01\x01\x12\r\n\x05limit\x18\x02 \x01(\x05\x42\x13\n\x11_next_create_time\"J\n\x11GetBookListResult\x12\x35\n\x06result\x18\x01 \x03(\x0b\x32%.book_manager_by_option.GetBookResult2\xd3\x03\n\x0b\x42ookManager\x12P\n\x0b\x63reate_book\x12).book_manager_by_option.CreateBookRequest\x1a\x16.google.protobuf.Empty\x12P\n\x0b\x64\x65lete_book\x12).book_manager_by_option.DeleteBookRequest\x1a\x16.google.protobuf.Empty\x12\x90\x01\n\x08get_book\x12&.book_manager_by_option.GetBookRequest\x1a%.book_manager_by_option.GetBookResult\"5\x8a\xd3\xe4\x93\x02/\"\x0b\n\t/book/get\xda\x01\x1f\n\x1dnot_use_field1,not_use_field2\x12\x8c\x01\n\rget_book_list\x12*.book_manager_by_option.GetBookListRequest\x1a).book_manager_by_option.GetBookListResult\"$\x8a\xd3\xe4\x93\x02\x1e\"\x10\n\x0e/book/get-list\xe2\x01\t\x12\x07/resultb\x06proto3')



_CREATEBOOKREQUEST = DESCRIPTOR.message_types_by_name['CreateBookRequest']
_DELETEBOOKREQUEST = DESCRIPTOR.message_types_by_name['DeleteBookRequest']
_GETBOOKREQUEST = DESCRIPTOR.message_types_by_name['GetBookRequest']
_GETBOOKRESULT = DESCRIPTOR.message_types_by_name['GetBookResult']
_GETBOOKLISTREQUEST = DESCRIPTOR.message_types_by_name['GetBookListRequest']
_GETBOOKLISTRESULT = DESCRIPTOR.message_types_by_name['GetBookListResult']
CreateBookRequest = _reflection.GeneratedProtocolMessageType('CreateBookRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEBOOKREQUEST,
  '__module__' : 'example.grpc_proto.example_proto_by_option.book.manager_pb2'
  # @@protoc_insertion_point(class_scope:book_manager_by_option.CreateBookRequest)
  })
_sym_db.RegisterMessage(CreateBookRequest)

DeleteBookRequest = _reflection.GeneratedProtocolMessageType('DeleteBookRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEBOOKREQUEST,
  '__module__' : 'example.grpc_proto.example_proto_by_option.book.manager_pb2'
  # @@protoc_insertion_point(class_scope:book_manager_by_option.DeleteBookRequest)
  })
_sym_db.RegisterMessage(DeleteBookRequest)

GetBookRequest = _reflection.GeneratedProtocolMessageType('GetBookRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBOOKREQUEST,
  '__module__' : 'example.grpc_proto.example_proto_by_option.book.manager_pb2'
  # @@protoc_insertion_point(class_scope:book_manager_by_option.GetBookRequest)
  })
_sym_db.RegisterMessage(GetBookRequest)

GetBookResult = _reflection.GeneratedProtocolMessageType('GetBookResult', (_message.Message,), {
  'DESCRIPTOR' : _GETBOOKRESULT,
  '__module__' : 'example.grpc_proto.example_proto_by_option.book.manager_pb2'
  # @@protoc_insertion_point(class_scope:book_manager_by_option.GetBookResult)
  })
_sym_db.RegisterMessage(GetBookResult)

GetBookListRequest = _reflection.GeneratedProtocolMessageType('GetBookListRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETBOOKLISTREQUEST,
  '__module__' : 'example.grpc_proto.example_proto_by_option.book.manager_pb2'
  # @@protoc_insertion_point(class_scope:book_manager_by_option.GetBookListRequest)
  })
_sym_db.RegisterMessage(GetBookListRequest)

GetBookListResult = _reflection.GeneratedProtocolMessageType('GetBookListResult', (_message.Message,), {
  'DESCRIPTOR' : _GETBOOKLISTRESULT,
  '__module__' : 'example.grpc_proto.example_proto_by_option.book.manager_pb2'
  # @@protoc_insertion_point(class_scope:book_manager_by_option.GetBookListResult)
  })
_sym_db.RegisterMessage(GetBookListResult)

_BOOKMANAGER = DESCRIPTOR.services_by_name['BookManager']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETBOOKREQUEST.fields_by_name['isbn']._options = None
  _GETBOOKREQUEST.fields_by_name['isbn']._serialized_options = b'\212C\035r\033\202\002\030grpc-gateway@field|Query'
  _BOOKMANAGER.methods_by_name['get_book']._options = None
  _BOOKMANAGER.methods_by_name['get_book']._serialized_options = b'\212\323\344\223\002/\"\013\n\t/book/get\332\001\037\n\035not_use_field1,not_use_field2'
  _BOOKMANAGER.methods_by_name['get_book_list']._options = None
  _BOOKMANAGER.methods_by_name['get_book_list']._serialized_options = b'\212\323\344\223\002\036\"\020\n\016/book/get-list\342\001\t\022\007/result'
  _CREATEBOOKREQUEST._serialized_start=282
  _CREATEBOOKREQUEST._serialized_end=392
  _DELETEBOOKREQUEST._serialized_start=394
  _DELETEBOOKREQUEST._serialized_end=427
  _GETBOOKREQUEST._serialized_start=429
  _GETBOOKREQUEST._serialized_end=541
  _GETBOOKRESULT._serialized_start=544
  _GETBOOKRESULT._serialized_end=748
  _GETBOOKLISTREQUEST._serialized_start=750
  _GETBOOKLISTREQUEST._serialized_end=865
  _GETBOOKLISTRESULT._serialized_start=867
  _GETBOOKLISTRESULT._serialized_end=941
  _BOOKMANAGER._serialized_start=944
  _BOOKMANAGER._serialized_end=1411
# @@protoc_insertion_point(module_scope)
