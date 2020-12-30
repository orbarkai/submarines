"""
The game object handles a game with another player
"""

from submarines_game.board import Board
import submarines_client


class SubmarinesGame:
    """
    A game instance, handles game logic and communication with another player
    """

    def __init__(self, client: submarines_client.BaseSubmarinesClient, verbose: bool = True):
        """
        Initialize the game

        :param client: The submarines client, must be connected to another player!
        :param verbose: if set to true, the logger will log info about the game
        """

        self._client = client
        self._verbose = verbose
