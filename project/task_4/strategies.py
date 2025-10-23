from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import random

try:
    from .enums import Rank
except ImportError:
    from enums import Rank

if TYPE_CHECKING:
    try:
        from .players import PlayerBase
        from .core import Deck
    except ImportError:
        from players import PlayerBase
        from core import Deck


class Strategy(ABC):
    """Abstract base class for bot strategies"""

    @abstractmethod
    def play(self, player: "PlayerBase", deck: "Deck") -> None:
        """
        Execute the strategy for a player

        Parameters:
            player (PlayerBase): The player using this strategy
            deck (Deck): The deck to draw cards from
        """
        pass


class SafePlayerStrategy(Strategy):
    """
    Safe Player strategy that plays conservatively
    Stands on 14+, rarely doubles down, splits only Aces and 8s
    """

    def play(self, player: "PlayerBase", deck: "Deck") -> None:
        """
        Execute safe playing strategy

        Parameters:
            player (PlayerBase): The player using this strategy
            deck (Deck): The deck to draw cards from
        """
        if player.can_split() and player.hand.cards[0].rank in [Rank.ACE, Rank.EIGHT]:
            player.split_hand()
            for hand in player.split_hands:
                self._play_single_hand(player, hand, deck)
            return

        self._play_single_hand(player, player.hand, deck)

    def _play_single_hand(self, player: "PlayerBase", hand, deck: "Deck") -> None:
        """
        Play a single hand with safe strategy

        Parameters:
            player (PlayerBase): The player using this strategy
            hand: The hand to play
            deck (Deck): The deck to draw cards from
        """
        if player.can_double() and len(hand.cards) == 2 and hand.get_score() == 11:
            player.double_bet()
            new_card = deck.deal_card()
            hand.add_card(new_card)
            return

        while hand.get_score() < 14 and not hand.is_busted():
            new_card = deck.deal_card()
            hand.add_card(new_card)


class RiskTakerStrategy(Strategy):
    """
    Risk Taker strategy that plays aggressively
    Hits until 19, often doubles down, loves splitting pairs
    """

    def play(self, player: "PlayerBase", deck: "Deck") -> None:
        """
        Execute risk taker playing strategy

        Parameters:
            player (PlayerBase): The player using this strategy
            deck (Deck): The deck to draw cards from
        """
        if player.can_split():
            player.split_hand()
            for hand in player.split_hands:
                self._play_single_hand(player, hand, deck)
            return

        self._play_single_hand(player, player.hand, deck)

    def _play_single_hand(self, player: "PlayerBase", hand, deck: "Deck") -> None:
        """
        Play a single hand with risk taker strategy

        Parameters:
            player (PlayerBase): The player using this strategy
            hand: The hand to play
            deck (Deck): The deck to draw cards from
        """
        if (
            player.can_double()
            and len(hand.cards) == 2
            and hand.get_score() in [9, 10, 11]
        ):
            player.double_bet()
            new_card = deck.deal_card()
            hand.add_card(new_card)
            return

        while hand.get_score() < 19 and not hand.is_busted():
            new_card = deck.deal_card()
            hand.add_card(new_card)


class UnpredictableStrategy(Strategy):
    """
    Unpredictable strategy that mixes random and strategic decisions
    Sometimes stands early, sometimes hits hard, makes surprising moves
    """

    def play(self, player: "PlayerBase", deck: "Deck") -> None:
        """
        Execute unpredictable playing strategy

        Parameters:
            player (PlayerBase): The player using this strategy
            deck (Deck): The deck to draw cards from
        """
        if player.can_split() and random.random() < 0.5:
            player.split_hand()
            for hand in player.split_hands:
                self._play_single_hand(player, hand, deck)
            return

        self._play_single_hand(player, player.hand, deck)

    def _play_single_hand(self, player: "PlayerBase", hand, deck: "Deck") -> None:
        """
        Play a single hand with unpredictable strategy

        Parameters:
            player (PlayerBase): The player using this strategy
            hand: The hand to play
            deck (Deck): The deck to draw cards from
        """
        current_score = hand.get_score()

        if (
            player.can_double()
            and len(hand.cards) == 2
            and current_score in [9, 10, 11]
            and random.random() < 0.4
        ):
            player.double_bet()
            new_card = deck.deal_card()
            hand.add_card(new_card)
            return

        while current_score < 21 and not hand.is_busted():
            stand_chance = min(0.3 + (current_score - 12) * 0.1, 0.8)

            if random.random() < stand_chance:
                break

            new_card = deck.deal_card()
            hand.add_card(new_card)
            current_score = hand.get_score()
