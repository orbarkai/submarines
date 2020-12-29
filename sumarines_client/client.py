"""
The main client class, handles all client functionality
"""


from abc import ABCMeta, abstractmethod
import socket

from sumarines_client import messages, constants
from sumarines_client.messages_codec import BaseMessagesCodec


class BaseSubmarinesClient(metaclass=ABCMeta):
    """
    The main client class, handles all client functionality
    """

    @classmethod
    @abstractmethod
    def listen(cls, listening_port: int):
        """
        Start listen to incoming tcp connections

        :param listening_port: The listening port to use
        :return: A client instance (on listen mode)
        """

        raise NotImplementedError()

    @abstractmethod
    def send_message(self, message: messages.BaseSubmarinesMessage):
        """
        send a message to the connected player

        :param message: The message you wish to send
        :raise NotConnectedError: No player is connected to the client
        """

        raise NotImplementedError()

    @abstractmethod
    def receive_message(self) -> messages.BaseSubmarinesMessage:
        """
        Receive a message from the connected player

        :return: The decoded message
        :raise NotConnectedError: No player is connected to the client
        """

        raise NotImplementedError()

    @abstractmethod
    def __enter__(self):
        """
        The client's entering point

        :return: The client
        """

        raise NotImplementedError()

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The client's exit point (used for cleanup)

        :return: Should the exception be suppressed
        """

        raise NotImplementedError()


class TCPSubmarinesClient(BaseSubmarinesClient):
    """
    The main client class, handles all client functionality,
    using tcp connection
    """

    def __init__(self,
                 messages_codec: BaseMessagesCodec,
                 listening_socket: socket.socket,
                 game_socket: socket.socket = None):
        """
        Initializing a client

        :param messages_codec: The messages codec of the client
        :param listening_socket: The socket in which you listen to incoming requests
        :param game_socket: A game socket, this socket has to be in a game session,
        means a game request and response was passed on this socket
        """

        self._messages_codec = messages_codec
        self._listening_socket = listening_socket
        self._game_socket = game_socket

    @classmethod
    def listen(cls, listening_port: int = constants.Network.DEFAULT_PORT):
        """
        Start listen to incoming tcp connections

        :param listening_port: The listening port to use
        :return: A client instance (on listen mode)
        """

        raise NotImplementedError()

    @abstractmethod
    def send_message(self, message: messages.BaseSubmarinesMessage):
        """
        send a message to the connected player

        :param message: The message you wish to send
        :raise NotConnectedError: No player is connected to the client
        """

        raise NotImplementedError()

    @abstractmethod
    def receive_message(self) -> messages.BaseSubmarinesMessage:
        """
        Receive a message from the connected player

        :return: The decoded message
        :raise NotConnectedError: No player is connected to the client
        """

        raise NotImplementedError()

    @abstractmethod
    def __enter__(self):
        """
        The client's entering point

        :return: The client
        """

        raise NotImplementedError()

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The client's exit point (used for cleanup)

        :return: Should the exception be suppressed
        """

        raise NotImplementedError()
