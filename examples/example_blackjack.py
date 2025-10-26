import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project.task_4.core import Card, Deck, Hand
from project.task_4.players import Player, Bot
from project.task_4.game import Game
from project.task_4.enums import StrategyType

if __name__ == "__main__":
    """
    Blackjack game main entry point

    Initializes and starts a Blackjack game with human player and AI bots
    """
    game = Game(max_rounds=5)
    player = Player("Player")
    game.add_player(player)
    game.start_game()
