"""
These are generic submarines client constants
"""

import enum

import messages

MAGIC_SIZE = 4


class Magic(enum.Enum):
    VERSION_ONE_MAGIC = 'BS1p'


class ProtocolFormats:
    MAGIC_FORMAT = '4s'
    MESSAGE_TYPE_FORMAT = 'B'

    RESPONSE_FORMAT = '?'

    COORDINATE_FORMAT = 'B'
    COORDINATE_DELIMITER = 4

    RESULT_CODE_FORMAT = 'B'
    SUBMARINE_SIZE_FORMAT = 'B'

    ERROR_CODE_FORMAT = 'B'


@enum.unique
class SubmarineSize(enum.IntEnum):
    NO_SUBMARINE = 0
    SUBMARINE_TWO = 2
    SUBMARINE_THREE = 3
    SUBMARINE_FOUR = 4
    SUBMARINE_FIVE = 5


@enum.unique
class ErrorCode(enum.IntEnum):
    GENERIC_ERROR = 0
    ALREADY_ATTACKED_ERROR = 1
    INVALID_COORDINATE_ERROR = 2


class MessagesCodec:
    MESSAGES_TYPES = {
        messages.GameRequestMessage.get_message_type(): messages.GameRequestMessage,
        messages.GameReplyMessage.get_message_type(): messages.GameReplyMessage,
        messages.OrderMessage.get_message_type(): messages.OrderMessage,
        messages.GuessMessage.get_message_type(): messages.GuessMessage,
        messages.ResultMessage.get_message_type(): messages.ResultMessage,
        messages.AcknowledgeMessage.get_message_type(): messages.AcknowledgeMessage,
        messages.ErrorMessage.get_message_type(): messages.ErrorMessage,
    }
