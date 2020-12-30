"""
These are generic submarines client constants
"""

import enum


class Protocol:
    MAGIC_SIZE = 4

    class Magic(enum.Enum):
        VERSION_ONE_MAGIC = 'BS1p'

    class Formats:
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


class Network:

    DEFAULT_PORT = 8300
    PUBLIC_IP = '0.0.0.0'

    BUFFER_SIZE = 1024
