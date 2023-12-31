# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: example/grpc_proto/example_proto/user/user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0example/grpc_proto/example_proto/user/user.proto\x12\x04user\x1a\x1bgoogle/protobuf/empty.proto\"a\n\x11\x43reateUserRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\x1a\n\x03sex\x18\x04 \x01(\x0e\x32\r.user.SexType\" \n\x11\x44\x65leteUserRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\"1\n\x10LoginUserRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"@\n\x0fLoginUserResult\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\x11\n\tuser_name\x18\x02 \x01(\t\x12\r\n\x05token\x18\x03 \x01(\t\"/\n\x11LogoutUserRequest\x12\x0b\n\x03uid\x18\x01 \x01(\t\x12\r\n\x05token\x18\x02 \x01(\t\"%\n\x14GetUidByTokenRequest\x12\r\n\x05token\x18\x01 \x01(\t\"\"\n\x13GetUidByTokenResult\x12\x0b\n\x03uid\x18\x01 \x01(\t*\x1d\n\x07SexType\x12\x07\n\x03man\x10\x00\x12\t\n\x05women\x10\x01\x32\xce\x02\n\x04User\x12I\n\x10get_uid_by_token\x12\x1a.user.GetUidByTokenRequest\x1a\x19.user.GetUidByTokenResult\x12>\n\x0blogout_user\x12\x17.user.LogoutUserRequest\x1a\x16.google.protobuf.Empty\x12;\n\nlogin_user\x12\x16.user.LoginUserRequest\x1a\x15.user.LoginUserResult\x12>\n\x0b\x63reate_user\x12\x17.user.CreateUserRequest\x1a\x16.google.protobuf.Empty\x12>\n\x0b\x64\x65lete_user\x12\x17.user.DeleteUserRequest\x1a\x16.google.protobuf.Emptyb\x06proto3')

_SEXTYPE = DESCRIPTOR.enum_types_by_name['SexType']
SexType = enum_type_wrapper.EnumTypeWrapper(_SEXTYPE)
man = 0
women = 1


_CREATEUSERREQUEST = DESCRIPTOR.message_types_by_name['CreateUserRequest']
_DELETEUSERREQUEST = DESCRIPTOR.message_types_by_name['DeleteUserRequest']
_LOGINUSERREQUEST = DESCRIPTOR.message_types_by_name['LoginUserRequest']
_LOGINUSERRESULT = DESCRIPTOR.message_types_by_name['LoginUserResult']
_LOGOUTUSERREQUEST = DESCRIPTOR.message_types_by_name['LogoutUserRequest']
_GETUIDBYTOKENREQUEST = DESCRIPTOR.message_types_by_name['GetUidByTokenRequest']
_GETUIDBYTOKENRESULT = DESCRIPTOR.message_types_by_name['GetUidByTokenResult']
CreateUserRequest = _reflection.GeneratedProtocolMessageType('CreateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERREQUEST,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.CreateUserRequest)
  })
_sym_db.RegisterMessage(CreateUserRequest)

DeleteUserRequest = _reflection.GeneratedProtocolMessageType('DeleteUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEUSERREQUEST,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.DeleteUserRequest)
  })
_sym_db.RegisterMessage(DeleteUserRequest)

LoginUserRequest = _reflection.GeneratedProtocolMessageType('LoginUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGINUSERREQUEST,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.LoginUserRequest)
  })
_sym_db.RegisterMessage(LoginUserRequest)

LoginUserResult = _reflection.GeneratedProtocolMessageType('LoginUserResult', (_message.Message,), {
  'DESCRIPTOR' : _LOGINUSERRESULT,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.LoginUserResult)
  })
_sym_db.RegisterMessage(LoginUserResult)

LogoutUserRequest = _reflection.GeneratedProtocolMessageType('LogoutUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _LOGOUTUSERREQUEST,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.LogoutUserRequest)
  })
_sym_db.RegisterMessage(LogoutUserRequest)

GetUidByTokenRequest = _reflection.GeneratedProtocolMessageType('GetUidByTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUIDBYTOKENREQUEST,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.GetUidByTokenRequest)
  })
_sym_db.RegisterMessage(GetUidByTokenRequest)

GetUidByTokenResult = _reflection.GeneratedProtocolMessageType('GetUidByTokenResult', (_message.Message,), {
  'DESCRIPTOR' : _GETUIDBYTOKENRESULT,
  '__module__' : 'example.grpc_proto.example_proto.user.user_pb2'
  # @@protoc_insertion_point(class_scope:user.GetUidByTokenResult)
  })
_sym_db.RegisterMessage(GetUidByTokenResult)

_USER = DESCRIPTOR.services_by_name['User']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SEXTYPE._serialized_start=461
  _SEXTYPE._serialized_end=490
  _CREATEUSERREQUEST._serialized_start=87
  _CREATEUSERREQUEST._serialized_end=184
  _DELETEUSERREQUEST._serialized_start=186
  _DELETEUSERREQUEST._serialized_end=218
  _LOGINUSERREQUEST._serialized_start=220
  _LOGINUSERREQUEST._serialized_end=269
  _LOGINUSERRESULT._serialized_start=271
  _LOGINUSERRESULT._serialized_end=335
  _LOGOUTUSERREQUEST._serialized_start=337
  _LOGOUTUSERREQUEST._serialized_end=384
  _GETUIDBYTOKENREQUEST._serialized_start=386
  _GETUIDBYTOKENREQUEST._serialized_end=423
  _GETUIDBYTOKENRESULT._serialized_start=425
  _GETUIDBYTOKENRESULT._serialized_end=459
  _USER._serialized_start=493
  _USER._serialized_end=827
# @@protoc_insertion_point(module_scope)
