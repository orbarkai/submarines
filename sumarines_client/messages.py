"""
This module has all the protocol's message types
"""

from abc import ABCMeta, abstractmethod
import enum

from sumarines_client import protocol_utils


@enum.unique
class SubmarineMessageType(enum.IntEnum):
    GAME_REQUEST = 0
    GAME_REPLY = 1
    ORDER = 2
    GUESS = 3
    RESULT = 4
    ACKNOWLEDGE = 5
    ERROR = 6


class BaseSubmarinesMessage(metaclass=ABCMeta):
    """
    The base class for all messages
    """

    @staticmethod
    @abstractmethod
    def get_message_type() -> SubmarineMessageType:
        """
        Get the message's type identifier

        :return: the message's type identifier
        """

        raise NotImplemented()

    @abstractmethod
    def encode(self) -> bytes:
        """
        Encode the message into bytes by the protocol (including magic and version)

        :return: the encoded message in bytes
        """

        raise NotImplemented()

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (including magic and version)
        :return: The message instance
        """

        raise NotImplemented()


class GameRequestMessage(metaclass=ABCMeta):
    """
    The initial game request message
    """

    MESSAGE_TYPE = SubmarineMessageType.GAME_REQUEST

    def __init__(self):
        pass

    @staticmethod
    def get_message_type() -> SubmarineMessageType:
        """
        Get the message's type identifier

        :return: the message's type identifier
        """

        return GameRequestMessage.MESSAGE_TYPE

    def encode(self) -> bytes:
        """
        Encode the message into bytes by the protocol (including magic and version)

        :return: the encoded message in bytes
        """

        encoded_headers = protocol_utils.encode_headers(self.get_message_type())
        return encoded_headers

    @classmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (including magic and version)
        :return: The message instance
        """

        return cls()
