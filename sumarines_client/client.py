"""
The main client class, handles all client functionality
"""


from abc import ABCMeta, abstractmethod

from sumarines_client import messages


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
