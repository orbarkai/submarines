"""
The main client class, handles all client functionality
"""


from abc import ABCMeta, abstractmethod
import socket
import logging

from sumarines_client import messages, constants, exceptions, protocol_utils
from sumarines_client.messages_codec import BaseMessagesCodec, MessagesCodec
from sumarines_client.messages import SubmarineMessageType


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
    def wait_for_game(self):
        """
        Wait for a game request, and accept it
        Note: this is a blocking method, it will exit only
        when a game connection is established
        """

        raise NotImplementedError()

    @abstractmethod
    def invite_player(self, player_host: str, player_port: int) -> bool:
        """
        Invite a player for a game
        Note: this is a blocking method, it will exit only
        when a response is received or an error is raised

        :param player_host: The player's host
        :param player_port: The player's port
        :return: whether the player accepted the game invite
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
    def receive_message(self, expected_type: SubmarineMessageType) -> messages.BaseSubmarinesMessage:
        """
        Receive a message from the connected player

        :param expected_type: optional, an expected message type
        :return: The decoded message
        :raise NotConnectedError: No player is connected to the client
        :raise ProtocolException: if the message is not expected type
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
        self._logger = logging.getLogger(constants.LOGGER_NAME)

    @classmethod
    def listen(cls,
               listening_port: int = constants.Network.DEFAULT_PORT,
               messages_codec: BaseMessagesCodec = MessagesCodec()):
        """
        Start listen to incoming tcp connections

        :param listening_port: The listening port to use
        :param messages_codec: The messages codec for the client
        :return: A client instance (on listen mode)
        """

        try:
            listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listening_socket.bind((constants.Network.PUBLIC_IP, listening_port))
            listening_socket.listen(1)

            return cls(messages_codec=messages_codec, listening_socket=listening_socket)
        except socket.error:
            raise

    def wait_for_game(self):
        """
        Wait for a game request, and accept it
        Note: this is a blocking method, it will exit only
        when a game connection is established
        """

        while not self._game_socket:
            try:
                # accept connection
                self._game_socket, address = self._listening_socket.accept()

                # receive game request
                self.receive_message(SubmarineMessageType.GAME_REQUEST)
                self._logger.info('Incoming game request: ', f'from {address}')

                # send game reply
                self.send_message(messages.GameReplyMessage())
                self._logger.info('Game reply sent: ', 'game starts')
            except exceptions.ProtocolException as pe:
                self._logger.warning('Protocol error: ', pe)
                self._game_socket = None
            except socket.error as se:
                self._logger.warning('Network error: ', se)
                self._game_socket = None

    def invite_player(self, player_host: str, player_port: int = constants.Network.DEFAULT_PORT) -> bool:
        """
        Invite a player for a game
        Note: this is a blocking method, it will exit only
        when a response is received or an error is raised

        :param player_host: The player's host
        :param player_port: The player's port
        :return: whether the player accepted the game invite
        """

        try:
            # Connect to player
            self._game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._game_socket.connect((player_host, player_port))

            # send game request
            self.send_message(messages.GameRequestMessage())

            # receive game reply
            game_reply: messages.GameReplyMessage = self.receive_message(SubmarineMessageType.GAME_REPLY)
            return game_reply.response
        except exceptions.ProtocolException:
            raise
        except socket.error:
            raise

    def send_message(self, message: messages.BaseSubmarinesMessage):
        """
        send a message to the connected player

        :param message: The message you wish to send
        :raise NotConnectedError: No player is connected to the client
        """

        encoded_message = self._messages_codec.encode_message(message)
        self._game_socket.send(encoded_message)

    def receive_message(self, expected_type: SubmarineMessageType = None) -> messages.BaseSubmarinesMessage:
        """
        Receive a message from the connected player

        :param expected_type: optional, an expected message type
        :return: The decoded message
        :raise NotConnectedError: No player is connected to the client
        :raise ProtocolException: if the message is not expected type
        """

        encoded_message = bytes()

        try:
            new_data = self._game_socket.recv(constants.Network.BUFFER_SIZE)

            while new_data:
                encoded_message += new_data

                if len(new_data) < constants.Network.BUFFER_SIZE:
                    break

                new_data = self._game_socket.recv(constants.Network.BUFFER_SIZE)

            message = self._messages_codec.decode_message(encoded_message)

            if message.get_message_type() == SubmarineMessageType.ERROR:
                raise message.exception

            if expected_type:
                protocol_utils.insure_message_type(message, expected_type)

            return message

        except exceptions.ProtocolException:
            raise
        except socket.error:
            raise

    def __enter__(self):
        """
        The client's entering point

        :return: The client
        """

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The client's exit point (used for cleanup)

        :return: Should the exception be suppressed
        """

        if self._game_socket:
            self._game_socket.close()

        if self._listening_socket:
            self._listening_socket.close()

        return False
