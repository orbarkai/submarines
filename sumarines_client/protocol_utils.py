"""
These are protocol utils (mostly encoding and decoding)
"""

import struct
from typing import Tuple

from sumarines_client import exceptions, constants
from sumarines_client.messages import SubmarineMessageType, BaseSubmarinesMessage
from sumarines_client.constants import Protocol


def calc_headers_size() -> int:
    """
    Get the headers size in the message

    :return: The size of the headers
    """

    headers_size = 0

    headers_size += Protocol.MAGIC_SIZE
    headers_size += struct.calcsize(Protocol.Formats.MESSAGE_TYPE_FORMAT)

    return headers_size


def encode_headers(message_type: SubmarineMessageType, version_magic: Protocol.Magic) -> bytes:
    """
    Encode the headers of the message

    :param message_type: The message's type
    :param version_magic: The version's magic
    :return: The encoded headers as bytes
    """

    encoded_headers = bytes()

    encoded_headers += version_magic.value.encode()
    encoded_headers += struct.pack(Protocol.Formats.MESSAGE_TYPE_FORMAT, message_type)

    return encoded_headers


def decode_headers(message: bytes) -> Tuple[Protocol.Magic, SubmarineMessageType]:
    """
    Decode the headers of a message

    :param message: The message you wish to decode
    :return: The magic and the message type
    :raise InvalidHeadersException: if the headers are not provided in the message
    """

    if len(message) < calc_headers_size():
        raise exceptions.InvalidHeadersException('The message\'s headers are not provided')

    encoded_headers = message[:calc_headers_size()]
    headers_format = f'{Protocol.Formats.MAGIC_FORMAT}{Protocol.Formats.MESSAGE_TYPE_FORMAT}'
    encoded_magic, message_type_value = struct.unpack(headers_format, encoded_headers)

    magic: Protocol.Magic = Protocol.Magic(encoded_magic.decode())
    message_type: SubmarineMessageType = SubmarineMessageType(message_type_value)

    return magic, message_type


def insure_message_type(message: BaseSubmarinesMessage, expected_message_type: SubmarineMessageType):
    """
    Raise a protocol error if the type of the message is unexpected

    :param message: The incoming message
    :param expected_message_type: The expected message type
    :raise: ProtocolException: if the type of the message is unexpected
    """

    if expected_message_type != message.get_message_type():
        raise exceptions.ProtocolException(f'Unexpected message type! '
                                           f'expected {expected_message_type},'
                                           f'got message.get_message_type()')

    return True
