import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "project", "task_4"))

from core import Card, Deck, Hand
from players import Player, Bot
from game import Game
from enums import StrategyType

if __name__ == "__main__":
    """
    Blackjack game main entry point

    Initializes and starts a Blackjack game with human player and AI bots
    """
    game = Game(max_rounds=5)
    player = Player("Player")
    game.add_player(player)
    game.start_game()
