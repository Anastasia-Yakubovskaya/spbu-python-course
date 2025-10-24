from typing import List
from core import Hand, Card, Deck
from enums import StrategyType
from strategies import (
    SafePlayerStrategy,
    RiskTakerStrategy,
    UnpredictableStrategy,
    Strategy,
)


class PlayerBase:
    """
    Base class for all players in Blackjack

    Attributes:
        name (str): Player name
        hand (Hand): Player's current hand
        bet (int): Current bet amount
        chips (int): Total chips available
        insurance_bet (int): Insurance bet amount
        has_doubled (bool): Whether player has doubled down
        has_surrendered (bool): Whether player has surrendered
        split_hands (List[Hand]): List of hands after splitting
        split_bets (List[int]): List of bets for split hands
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a player with default attributes

        Parameters:
            name (str): Player name
        """
        self.name: str = name
        self.hand: Hand = Hand()
        self.bet: int = 0
        self.chips: int = 1000
        self.insurance_bet: int = 0
        self.has_doubled: bool = False
        self.has_surrendered: bool = False
        self.split_hands: List[Hand] = []
        self.split_bets: List[int] = []

    def place_bet(self, amount: int) -> bool:
        """
        Place a bet for the current round

        Parameters:
            amount (int): Amount to bet

        Returns:
            bool: True if bet was placed successfully, False otherwise
        """
        if amount <= self.chips:
            self.bet = amount
            self.chips -= amount
            return True
        return False

    def place_insurance(self) -> bool:
        """
        Place an insurance bet (half of original bet)

        Returns:
            bool: True if insurance was placed successfully, False otherwise
        """
        insurance_amount = self.bet // 2
        if insurance_amount <= self.chips:
            self.insurance_bet = insurance_amount
            self.chips -= insurance_amount
            return True
        return False

    def can_double(self) -> bool:
        """
        Check if player can double down

        Returns:
            bool: True if player can double down, False otherwise
        """
        return (
            len(self.hand.cards) == 2
            and not self.has_doubled
            and self.bet * 2 <= self.chips
        )

    def double_bet(self) -> bool:
        """
        Double the current bet and take one more card

        Returns:
            bool: True if double was successful, False otherwise
        """
        if self.can_double():
            additional_bet = self.bet
            if additional_bet <= self.chips:
                self.chips -= additional_bet
                self.bet += additional_bet
                self.has_doubled = True
                return True
        return False

    def can_split(self) -> bool:
        """
        Check if player can split their hand

        Returns:
            bool: True if hand can be split, False otherwise
        """
        return (
            self.hand.can_split()
            and len(self.split_hands) == 0
            and self.bet * 2 <= self.chips
        )

    def split_hand(self) -> bool:
        """
        Split the current hand into two separate hands

        Returns:
            bool: True if split was successful, False otherwise
        """
        if self.can_split():
            additional_bet = self.bet
            if additional_bet <= self.chips:
                self.chips -= additional_bet

                hand1 = Hand()
                hand2 = Hand()

                hand1.add_card(self.hand.cards[0])
                hand2.add_card(self.hand.cards[1])

                self.split_hands = [hand1, hand2]
                self.split_bets = [self.bet, self.bet]
                self.hand.clear()
                return True
        return False

    def surrender(self) -> bool:
        """
        Surrender the hand and lose half the bet

        Returns:
            bool: True if surrender was successful, False otherwise
        """
        if len(self.hand.cards) == 2 and not self.has_doubled:
            self.has_surrendered = True
            return True
        return False

    def clear_hand(self) -> None:
        """Clear all hands and reset betting state for new round"""
        self.hand.clear()
        self.split_hands.clear()
        self.split_bets.clear()


class Bot(PlayerBase):
    """
    AI player with different playing strategies

    Attributes:
        strategy (StrategyType): Bot's playing strategy
        _strategy_obj (Strategy): Strategy object
    """

    def __init__(self, name: str, strategy: StrategyType = StrategyType.SAFE) -> None:
        """
        Initialize a bot player

        Parameters:
            name (str): Bot's name
            strategy (StrategyType): Playing strategy
        """
        super().__init__(name)
        self.strategy: StrategyType = strategy
        self._strategy_obj = self._create_strategy(strategy)

    def _create_strategy(self, strategy: StrategyType) -> "Strategy":
        """
        Create strategy instance based on type

        Parameters:
            strategy (StrategyType): Strategy type

        Returns:
            Strategy: Strategy object instance
        """
        if strategy == StrategyType.SAFE:
            return SafePlayerStrategy()
        elif strategy == StrategyType.RISK_TAKER:
            return RiskTakerStrategy()
        elif strategy == StrategyType.UNPREDICTABLE:
            return UnpredictableStrategy()
        else:
            return SafePlayerStrategy()

    def calculate_bet(self) -> int:
        """
        Calculate bet amount based on bot's strategy

        Returns:
            int: Bet amount
        """
        return self._strategy_obj.calculate_bet(self)

    def play(self, deck: Deck) -> None:
        """
        Execute bot's playing strategy

        Parameters:
            deck (Deck): Deck to draw cards from
        """
        print(f"{self.name} ({self.strategy.value}): ", end="")
        if self.strategy == StrategyType.SAFE:
            print("Bot with safe strategy")
        elif self.strategy == StrategyType.RISK_TAKER:
            print("Bot with risk_taker strategy")
        elif self.strategy == StrategyType.UNPREDICTABLE:
            print("Bot with unpredictable strategy")

        self._strategy_obj.play(self, deck)

        if self.split_hands:
            for i, hand in enumerate(self.split_hands):
                split_text = f" (split {i + 1})" if len(self.split_hands) > 1 else ""
                print(
                    f"{self.name}{split_text}: {[str(card) for card in hand.cards]} (Score: {hand.get_score()})"
                )
        else:
            print(
                f"{self.name}: {[str(card) for card in self.hand.cards]} (Score: {self.hand.get_score()})"
            )


class Player(PlayerBase):
    """
    Human player that interacts through console input
    """

    def __init__(self, name: str) -> None:
        """
        Initialize a human player

        Parameters:
            name (str): Player's name
        """
        super().__init__(name)

    def take_turn(self, deck: Deck, dealer_up_card: Card) -> None:
        """
        Execute player's turn with console interaction

        Parameters:
            deck (Deck): Deck to draw cards from
            dealer_up_card (Card): Dealer's visible card
        """
        if self.split_hands:
            for i, split_hand in enumerate(self.split_hands):
                print(f"Playing split hand {i + 1}")
                self._play_single_hand(deck, dealer_up_card, split_hand, True)
            return

        self._play_single_hand(deck, dealer_up_card, self.hand, False)

    def _play_single_hand(
        self, deck: Deck, dealer_up_card: Card, hand: Hand, is_split: bool
    ) -> None:
        """
        Play a single hand with user interaction

        Parameters:
            deck (Deck): Deck to draw cards from
            dealer_up_card (Card): Dealer's visible card
            hand (Hand): Hand to play
            is_split (bool): Whether this is a split hand
        """
        while not hand.is_busted() and not self.has_surrendered:
            print(
                f"{self.name}: {[str(card) for card in hand.cards]} (Score: {hand.get_score()})"
            )

            actions = ["hit", "stand"]
            if self.can_double() and not is_split:
                actions.append("double")
            if self.can_split() and not is_split:
                actions.append("split")
            if len(hand.cards) == 2 and not self.has_doubled and not is_split:
                actions.append("surrender")

            action = input(f"Action ({'/'.join(actions)}): ").lower()

            if action == "hit":
                card = deck.deal_card()
                hand.add_card(card)
                print(f"Got: {card}")

                if hand.is_five_card_charlie():
                    print("Five Card - automatic win!")
                    return

                if hand.is_busted():
                    print("Busted!")
                    break

            elif action == "stand":
                break

            elif action == "double" and "double" in actions:
                if self.double_bet():
                    card = deck.deal_card()
                    hand.add_card(card)
                    print(f"Doubled - got: {card}")
                    break

            elif action == "split" and "split" in actions:
                if self.split_hand():
                    print("Hand split")
                    return

            elif action == "surrender" and "surrender" in actions:
                if self.surrender():
                    print("Surrendered - lose half bet")
                    break
