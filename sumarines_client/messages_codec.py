"""
The messages codec is responsible for encoding and decoding messages
"""

from abc import ABCMeta, abstractmethod

from sumarines_client import protocol_utils
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
