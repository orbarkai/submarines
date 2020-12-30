"""
A game board's functionality
"""

from submarines_game import constatns
import numpy as np

class Board:
    """
    The board keeps memory on all submarines.
    It helps you place submarines and mark tiles
    Each tile on the board represents the submarine's size
    """

    def __init__(self, size: int = constatns.Board.BOARD_SIZE):
        self._size = size
        self.tiles = np.full((self._size, self._size), constatns.Board.NO_SUBMARINE, dtype=int)

    def place_submarine(self, column: int, row: int, size: int, horizontal: bool = True):
        """
        Place a submarine on the board if possible

        :param row: The submarine's top left position row
        :param column: The submarine's top left position column
        :param size: The submarine's size
        :param horizontal: Is the submarine placed horizontally
        """

        if horizontal:
            for x in range(column, column + size):
                if x < self._size and row < self._size \
                        and self.tiles[x][row] == constatns.Board.NO_SUBMARINE:

                    self.tiles[x][row] = size
        else:
            for y in range(row, row + size):
                if y < self._size and column < self._size \
                        and self.tiles[column][y] == constatns.Board.NO_SUBMARINE:

                    self.tiles[column][y] = size
