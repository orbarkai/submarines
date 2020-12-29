"""
All the client's exceptions are in this module
"""


class SubmarinesClientException(Exception):
    """
    The base submarine client exception
    """

    pass


class ProtocolException(SubmarinesClientException):
    """
    A generic protocol error
    """

    pass