import os
import sys


# Добавляем путь к task_4
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "project", "task_4"))

# Используем прямые импорты
from core import Card, Deck, Hand
from players import Player, Bot
from game import Game
from enums import StrategyType

if __name__ == "__main__":
    game = Game(max_rounds=5)
    player = Player("Player")
    game.add_player(player)
    game.start_game()
