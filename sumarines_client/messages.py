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
    The initial game request message's reply
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


class OrderMessage(BaseSubmarinesMessage):
    """
    The order inform message
    """

    MESSAGE_TYPE = SubmarineMessageType.ORDER

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


class GuessMessage(BaseSubmarinesMessage):
    """
    The player's guess message
    """

    MESSAGE_TYPE = SubmarineMessageType.GUESS

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

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

        coordinate = self.column % (2 ** constants.ProtocolFormats.COORDINATE_DELIMITER)
        coordinate += (self.row << constants.ProtocolFormats.COORDINATE_DELIMITER)

        encoded_message = struct.pack(constants.ProtocolFormats.COORDINATE_FORMAT, coordinate)

        return encoded_message

    @classmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (not including headers)
        :return: The message instance
        """

        coordinate, = struct.unpack(constants.ProtocolFormats.COORDINATE_FORMAT, data)
        column = coordinate % (2 ** constants.ProtocolFormats.COORDINATE_DELIMITER)
        row = coordinate >> constants.ProtocolFormats.COORDINATE_DELIMITER
        return cls(row=row, column=column)


class ResultMessage(BaseSubmarinesMessage):
    """
    The player's guess message's result
    """

    MESSAGE_TYPE = SubmarineMessageType.RESULT

    def __init__(self, submarine_size: constants.SubmarineSize = constants.SubmarineSize.NO_SUBMARINE,
                 did_sink: bool = False,
                 did_sink_last: bool = False):

        self.submarine_size = submarine_size
        self.did_sink = did_sink
        self.did_sink_last = did_sink_last

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

        result_code = bool(self.submarine_size) + self.did_sink + self.did_sink_last
        encoded_message = struct.pack(constants.ProtocolFormats.RESULT_CODE_FORMAT, result_code)

        if bool(self.submarine_size):
            encoded_message += struct.pack(constants.ProtocolFormats.SUBMARINE_SIZE_FORMAT, self.submarine_size)

        return encoded_message

    @classmethod
    def decode(cls, data: bytes):
        """
        Decode bytes to a message instance

        :param data: The data you wish to encode (not including headers)
        :return: The message instance
        """

        result_code, = struct.unpack(constants.ProtocolFormats.RESULT_CODE_FORMAT, data[:1])
        result_message = cls()

        if result_code > 0:
            submarine_size_value, = struct.unpack(constants.ProtocolFormats.SUBMARINE_SIZE_FORMAT, data[1:])
            result_message.submarine_size = constants.SubmarineSize(submarine_size_value)

        if result_code > 1:
            result_message.did_sink = True

        if result_code > 2:
            result_message.did_sink_last = True

        return result_message
