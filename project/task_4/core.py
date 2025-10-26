import random
from typing import List
from project.task_4.enums import Suit, Rank


class Card:
    """
    Represents a playing card with suit and rank

    Attributes:
        suit (Suit): The suit of the card
        rank (Rank): The rank of the card
    """

    def __init__(self, suit: Suit, rank: Rank) -> None:
        """
        Initialize a card with suit and rank

        Parameters:
            suit (Suit): The suit of the card
            rank (Rank): The rank of the card
        """
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        """
        Get string representation of the card

        Returns:
            str: String representation in format 'Rank of Suit'
        """
        return f"{self.rank.value} of {self.suit.value}"

    def get_value(self) -> int:
        """
        Get the numerical value of the card

        Returns:
            int: Value of the card (2-10, 10 for face cards, 11 for Ace)
        """
        if self.rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
            return 10
        elif self.rank == Rank.ACE:
            return 11
        else:
            return int(self.rank.value)

    def is_same_rank(self, other_card: "Card") -> bool:
        """
        Check if two cards have the same rank

        Parameters:
            other_card (Card): Another card to compare with

        Returns:
            bool: True if cards have same rank, False otherwise
        """
        return self.rank == other_card.rank


class Deck:
    """
    Represents a deck of 52 playing cards

    Attributes:
        cards (List[Card]): List of cards in the deck
    """

    def __init__(self) -> None:
        """Initialize a new shuffled deck of 52 cards"""
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        """
        Deal one card from the deck

        Returns:
            Card: The top card from the deck
        """
        return self.cards.pop()

    def cards_remaining(self) -> int:
        """
        Get the number of cards remaining in the deck

        Returns:
            int: Number of cards left in the deck
        """
        return len(self.cards)


class Hand:
    """
    Represents a hand of cards in Blackjack

    Attributes:
        cards (List[Card]): List of cards in the hand
    """

    def __init__(self) -> None:
        """Initialize an empty hand"""
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        """
        Add a card to the hand

        Parameters:
            card (Card): Card to add to the hand
        """
        self.cards.append(card)

    def get_score(self) -> int:
        """
        Calculate the total score of the hand

        Returns:
            int: Total score with Aces adjusted to prevent busting
        """
        score = 0
        aces = 0

        for card in self.cards:
            if card.rank == Rank.ACE:
                aces += 1
                score += 11
            elif card.rank in [Rank.JACK, Rank.QUEEN, Rank.KING]:
                score += 10
            else:
                score += int(card.rank.value)

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    def is_blackjack(self) -> bool:
        """
        Check if hand is a Blackjack (Ace + 10-value card)

        Returns:
            bool: True if hand is Blackjack, False otherwise
        """
        return len(self.cards) == 2 and self.get_score() == 21

    def is_busted(self) -> bool:
        """
        Check if hand is busted (score over 21)

        Returns:
            bool: True if hand is busted, False otherwise
        """
        return self.get_score() > 21

    def can_split(self) -> bool:
        """
        Check if hand can be split (two cards of same rank)

        Returns:
            bool: True if hand can be split, False otherwise
        """
        return len(self.cards) == 2 and self.cards[0].is_same_rank(self.cards[1])

    def is_five_card_charlie(self) -> bool:
        """
        Check if hand is a Five Card Charlie (5+ cards without busting)

        Returns:
            bool: True if Five Card Charlie, False otherwise
        """
        return len(self.cards) >= 5 and not self.is_busted()

    def clear(self) -> None:
        """Clear all cards from the hand"""
        self.cards.clear()
