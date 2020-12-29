"""
These are generic submarines client constants
"""

import enum


class Magics:
    VERSION_ONE_MAGIC = 'BS1p'


class ProtocolFormats:
    MAGIC_FORMAT = '4s'
    MESSAGE_TYPE_FORMAT = 'B'

    RESPONSE_FORMAT = '?'

    COORDINATE_FORMAT = 'B'
    COORDINATE_DELIMITER = 4

    RESULT_CODE_FORMAT = 'B'
    SUBMARINE_SIZE_FORMAT = 'B'


@enum.unique
class SubmarineSize(enum.IntEnum):
    NO_SUBMARINE = 0
    SUBMARINE_TWO = 2
    SUBMARINE_THREE = 3
    SUBMARINE_FOUR = 4
    SUBMARINE_FIVE = 5
