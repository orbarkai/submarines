"""
The client's entry point
"""

from submarines_client.client import BaseSubmarinesClient, TCPSubmarinesClient
from submarines_client.messages_codec import BaseMessagesCodec, MessagesCodec
from submarines_client import messages, constants, exceptions, protocol_utils

