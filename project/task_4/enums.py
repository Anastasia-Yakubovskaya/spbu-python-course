from enum import Enum


class Suit(Enum):
    """
    Represents the four suits in a standard deck of playing cards

    Attributes:
        HEARTS: Hearts suit
        DIAMONDS: Diamonds suit
        CLUBS: Clubs suit
        SPADES: Spades suit
    """

    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Rank(Enum):
    """
    Represents the thirteen ranks in a standard deck of playing cards

    Attributes:
        TWO: Rank 2
        THREE: Rank 3
        FOUR: Rank 4
        FIVE: Rank 5
        SIX: Rank 6
        SEVEN: Rank 7
        EIGHT: Rank 8
        NINE: Rank 9
        TEN: Rank 10
        JACK: Jack face card
        QUEEN: Queen face card
        KING: King face card
        ACE: Ace card
    """

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class StrategyType(Enum):
    """
    Represents different playing strategies for AI players

    Attributes:
        SAFE: Conservative playing strategy
        RISK_TAKER: Aggressive playing strategy
        UNPREDICTABLE: Random mixed strategy
    """

    SAFE = "safe"
    RISK_TAKER = "risk_taker"
    UNPREDICTABLE = "unpredictable"
