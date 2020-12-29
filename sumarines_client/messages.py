"""
This module has all the protocol's message types
"""

from abc import ABCMeta, abstractmethod
import enum
import struct

from sumarines_client import constants


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
        Encode the message into bytes by the protocol (not including headers)

        :return: the encoded message in bytes
        """

        raise NotImplemented()

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (not including headers)
        :return: The message instance
        """

        raise NotImplemented()


class GameRequestMessage(BaseSubmarinesMessage):
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
        Encode the message into bytes by the protocol (not including headers)

        :return: the encoded message in bytes
        """

        return bytes()

    @classmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (not including headers)
        :return: The message instance
        """

        return cls()


class GameReplyMessage(BaseSubmarinesMessage):
    """
    The initial game request message
    """

    MESSAGE_TYPE = SubmarineMessageType.GAME_REPLY

    def __init__(self, response: bool):
        self.response = response

    @staticmethod
    def get_message_type() -> SubmarineMessageType:
        """
        Get the message's type identifier

        :return: the message's type identifier
        """

        return GameRequestMessage.MESSAGE_TYPE

    def encode(self) -> bytes:
        """
        Encode the message into bytes by the protocol (not including headers)

        :return: the encoded message in bytes
        """

        encoded_message = struct.pack(constants.ProtocolFormats.RESPONSE_FORMAT, self.response)
        return encoded_message

    @classmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (not including headers)
        :return: The message instance
        """

        response, = struct.unpack(constants.ProtocolFormats.RESPONSE_FORMAT, data)
        return cls(response=response)
