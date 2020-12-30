"""
A game board's functionality
"""

from submarines_game import constatns
import numpy as np
import enum


@enum.unique
class Tile(enum.IntEnum):
    """
    A tile on the board is represented as an int enum.
    """

    EMPTY_TILE = 0
    SUBMARINE_TWO_TILE = 1
    SUBMARINE_THREE_TILE = 2
    SUBMARINE_FOUR_TILE = 3
    SUBMARINE_FIVE_TILE = 4


class Board:
    """
    The board keeps memory on all submarines.
    It helps you place submarines and mark tiles
    """

    def __init__(self, size: int = constatns.Board.BOARD_SIZE):
        self.tiles = np.full((size, size), Tile.EMPTY_TILE, dtype=Tile)
