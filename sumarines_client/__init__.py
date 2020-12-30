"""
The client's entry point
"""

from sumarines_client.client import BaseSubmarinesClient, TCPSubmarinesClient
from sumarines_client.messages_codec import BaseMessagesCodec, MessagesCodec
from sumarines_client import messages, constants, exceptions, protocol_utils

