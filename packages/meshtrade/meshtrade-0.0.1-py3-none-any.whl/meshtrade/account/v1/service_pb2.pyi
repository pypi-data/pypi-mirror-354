from meshtrade.account.v1 import account_pb2 as _account_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRequest(_message.Message):
    __slots__ = ("number",)
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    number: str
    def __init__(self, number: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ("account",)
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    account: _account_pb2.Account
    def __init__(self, account: _Optional[_Union[_account_pb2.Account, _Mapping]] = ...) -> None: ...
