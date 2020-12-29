"""
These are protocol utils (mostly encoding and decoding)
"""

import struct
from typing import Tuple

from sumarines_client import exceptions, constants
from sumarines_client.messages import SubmarineMessageType


def calc_headers_size() -> int:
    """
    Get the headers size in the message

    :return: The size of the headers
    """

    headers_size = 0

    headers_size += constants.MAGIC_SIZE
    headers_size += struct.calcsize(constants.ProtocolFormats.MESSAGE_TYPE_FORMAT)

    return headers_size


def encode_headers(message_type: SubmarineMessageType, version_magic: constants.Magic) -> bytes:
    """
    Encode the headers of the message

    :param message_type: The message's type
    :param version_magic: The version's magic
    :return: The encoded headers as bytes
    """

    encoded_headers = bytes()

    encoded_headers += version_magic.value.encode()
    encoded_headers += struct.pack(constants.ProtocolFormats.MESSAGE_TYPE_FORMAT, message_type)

    return encoded_headers


def decode_headers(message: bytes) -> Tuple[constants.Magic, SubmarineMessageType]:
    """
    Decode the headers of a message

    :param message: The message you wish to decode
    :return: The magic and the message type
    :raise InvalidHeadersException: if the headers are not provided in the message
    """

    if len(message) < calc_headers_size():
        raise exceptions.InvalidHeadersException('The message\'s headers are not provided')

    encoded_headers = message[:calc_headers_size()]
    headers_format = f'{constants.ProtocolFormats.MAGIC_FORMAT}{constants.ProtocolFormats.MESSAGE_TYPE_FORMAT}'
    encoded_magic, message_type_value = struct.unpack(headers_format, encoded_headers)

    magic: constants.Magic = constants.Magic(encoded_magic.decode())
    message_type: SubmarineMessageType = SubmarineMessageType(message_type_value)

    return magic, message_type
