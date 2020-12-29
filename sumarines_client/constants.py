"""
These are generic submarines client constants
"""


class Magics:
    VERSION_ONE_MAGIC = 'BS1p'


class ProtocolFormats:
    MAGIC_FORMAT = '4s'
    MESSAGE_TYPE_FORMAT = 'B'

    RESPONSE_FORMAT = '?'

    COORDINATE_FORMAT = 'B'
    COORDINATE_DELIMITER = 4
