import os
import sys

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "project", "task_4")
sys.path.insert(0, os.path.abspath(project_path))

from blackjack import Card, Deck, Hand, PlayerBase, Bot, Player, Game

game = Game(max_rounds=5)
player = Player("Player")
game.add_player(player)
game.start_game()
