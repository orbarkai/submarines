"""
The messages codec is responsible for encoding and decoding messages
"""

from abc import ABCMeta, abstractmethod

from sumarines_client import protocol_utils, constants, exceptions
from sumarines_client.messages import BaseSubmarinesMessage


class BaseMessagesCodec(metaclass=ABCMeta):
    """
    A base class for all message codecs,
    The messages codec is responsible for encoding and decoding messages
    """

    @abstractmethod
    def encode_message(self, message: BaseSubmarinesMessage) -> bytes:
        """
        encodes a single message (with headers)

        :param message: The message you wish to encode
        :return: The encoded message as bytes
        """

        raise NotImplementedError()

    @abstractmethod
    def decode_message(self, message: bytes) -> BaseSubmarinesMessage:
        """
        decodes a single message (with headers)

        :param message: The message you wish to decode
        :return: The decoded message instance
        """

        raise NotImplementedError()


class MessagesCodec(BaseMessagesCodec):
    """
    The messages codec is responsible for encoding and decoding messages
    """

    def __init__(self, version_magic: constants.Magic = constants.Magic.VERSION_ONE_MAGIC):
        self._version_magic = version_magic

    def encode_message(self, message: BaseSubmarinesMessage) -> bytes:
        """
        encodes a single message (with headers)

        :param message: The message you wish to encode
        :return: The encoded message as bytes
        """

        encoded_message = bytes()

        encoded_message += protocol_utils.encode_headers(message.get_message_type(), self._version_magic)
        encoded_message += message.encode()

        return encoded_message

    def decode_message(self, message: bytes) -> BaseSubmarinesMessage:
        """
        decodes a single message (with headers)

        :param message: The message you wish to decode
        :return: The decoded message instance
        :raise InvalidMessageTypeException: if the message type is invalid
        :raise InvalidMagicException: if the magic is not matching the current magic
        :raise InvalidHeadersException: if the headers are not provided in the message
        """

        try:
            magic, message_type = protocol_utils.decode_headers(message)

            if magic != self._version_magic:
                raise exceptions.InvalidMagicException('The given version magic is different from the current one')

            if message_type not in constants.MessagesCodec.MESSAGES_TYPES:
                raise exceptions.InvalidMessageTypeException('The message type provided is invalid')

            encoded_message_data = message[protocol_utils.calc_headers_size():]
            message_type = constants.MessagesCodec.MESSAGES_TYPES[message_type]

            decoded_message = message_type.decode(encoded_message_data)
            return decoded_message
        except exceptions.ProtocolException:
            raise
