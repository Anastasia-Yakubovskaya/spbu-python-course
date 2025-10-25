import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from project.task_4.core import Card, Deck, Hand
from project.task_4.players import PlayerBase, Player, Bot
from project.task_4.game import Game
from project.task_4.enums import Suit, Rank, StrategyType


class TestCard:
    """
    Test cases for the Card class.

    Test cases:
    - Card creation with valid suit and rank
    - String representation of cards
    - Value calculation for different card ranks
    - Rank comparison between cards
    """

    def test_card_creation(self):
        """Test that cards are created with correct suit and rank attributes."""
        card = Card(Suit.HEARTS, Rank.ACE)
        assert card.suit == Suit.HEARTS
        assert card.rank == Rank.ACE

    def test_card_string_representation(self):
        """Test the string representation of cards."""
        card = Card(Suit.DIAMONDS, Rank.KING)
        assert str(card) == "K of Diamonds"

    def test_card_values(self):
        """Test value calculation for all card ranks including face cards and aces."""
        test_cases = [
            (Rank.TWO, 2),
            (Rank.TEN, 10),
            (Rank.JACK, 10),
            (Rank.QUEEN, 10),
            (Rank.KING, 10),
            (Rank.ACE, 11),
        ]
        for rank, expected_value in test_cases:
            card = Card(Suit.HEARTS, rank)
            assert card.get_value() == expected_value

    def test_card_same_rank(self):
        """Test rank comparison between different cards."""
        card_k = Card(Suit.HEARTS, Rank.KING)
        card_q = Card(Suit.DIAMONDS, Rank.QUEEN)
        card_a = Card(Suit.CLUBS, Rank.ACE)
        card_2 = Card(Suit.SPADES, Rank.TWO)

        assert card_k.is_same_rank(card_q) == False
        assert card_k.is_same_rank(card_a) == False
        assert card_a.is_same_rank(card_2) == False


class TestDeck:
    """
    Test cases for the Deck class.

    Test cases:
    - Deck initialization with correct number of cards
    - Card dealing functionality
    - Cards remaining count tracking
    """

    def test_deck_initialization(self):
        """Test that deck is initialized with 52 cards."""
        deck = Deck()
        assert len(deck.cards) == 52

    def test_deck_deal_card(self):
        """Test that dealing a card reduces deck size and returns a Card instance."""
        deck = Deck()
        initial_count = len(deck.cards)
        card = deck.deal_card()

        assert isinstance(card, Card)
        assert len(deck.cards) == initial_count - 1

    def test_deck_cards_remaining(self):
        """Test cards_remaining method returns correct count."""
        deck = Deck()
        assert deck.cards_remaining() == 52
        deck.deal_card()
        assert deck.cards_remaining() == 51


class TestHand:
    """
    Test cases for the Hand class.

    Test cases:
    - Hand initialization with empty state
    - Adding cards to hand
    - Blackjack detection
    - Bust detection
    - Ace value adjustment
    - Split eligibility
    - Five-card Charlie detection
    - Hand clearing functionality
    """

    def test_hand_initialization(self):
        """Test that hand starts empty with zero score."""
        hand = Hand()
        assert hand.cards == []
        assert hand.get_score() == 0

    def test_hand_add_card(self):
        """Test adding cards to hand increases card count."""
        hand = Hand()
        card = Card(Suit.HEARTS, Rank.ACE)
        hand.add_card(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card

    def test_hand_blackjack_detection(self):
        """Test blackjack detection with ace and face card."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.DIAMONDS, Rank.KING))
        assert hand.is_blackjack() == True
        assert hand.get_score() == 21

    def test_hand_bust_detection(self):
        """Test bust detection when hand exceeds 21."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.KING))
        hand.add_card(Card(Suit.DIAMONDS, Rank.QUEEN))
        hand.add_card(Card(Suit.CLUBS, Rank.TWO))
        assert hand.is_busted() == True
        assert hand.get_score() > 21

    def test_hand_ace_adjustment(self):
        """Test ace value adjustment from 11 to 1 when beneficial."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.DIAMONDS, Rank.ACE))
        hand.add_card(Card(Suit.CLUBS, Rank.NINE))
        assert hand.get_score() == 21

    def test_hand_split_detection(self):
        """Test split eligibility with matching and non-matching ranks."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.EIGHT))
        hand.add_card(Card(Suit.DIAMONDS, Rank.EIGHT))
        assert hand.can_split() == True

        hand.clear()
        hand.add_card(Card(Suit.HEARTS, Rank.EIGHT))
        hand.add_card(Card(Suit.DIAMONDS, Rank.NINE))
        assert hand.can_split() == False

    def test_hand_five_card_charlie(self):
        """Test five-card Charlie detection with exactly 5 cards under 21."""
        hand = Hand()
        for rank in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX]:
            hand.add_card(Card(Suit.HEARTS, rank))
        assert hand.is_five_card_charlie() == True

        hand.clear()
        for rank in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.KING]:
            hand.add_card(Card(Suit.HEARTS, rank))
        assert hand.is_five_card_charlie() == False

    def test_hand_clear(self):
        """Test hand clearing resets cards and score."""
        hand = Hand()
        hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        hand.add_card(Card(Suit.DIAMONDS, Rank.KING))
        hand.clear()
        assert hand.cards == []
        assert hand.get_score() == 0


class TestPlayerBase:
    """
    Test cases for the PlayerBase class.

    Test cases:
    - Player initialization with default attributes
    - Bet placement and validation
    - Insurance bet functionality
    - Double down capability
    - Hand splitting
    - Surrender option
    - Hand clearing between rounds
    """

    @pytest.fixture
    def player(self):
        return PlayerBase("TestPlayer")

    def test_player_initialization(self, player):
        """Test player initialization with default chip count and empty hand."""
        assert player.name == "TestPlayer"
        assert player.chips == 1000
        assert player.bet == 0
        assert isinstance(player.hand, Hand)

    def test_player_place_bet(self, player):
        """Test bet placement deducts from chips and sets bet amount."""
        assert player.place_bet(100) == True
        assert player.bet == 100
        assert player.chips == 900

    def test_player_insurance(self, player):
        """Test insurance bet placement at half the original bet."""
        player.place_bet(100)
        assert player.place_insurance() == True
        assert player.insurance_bet == 50
        assert player.chips == 850

    def test_player_double_down(self, player):
        """Test double down doubles the bet and marks player as doubled."""
        player.place_bet(100)
        player.hand.add_card(Card(Suit.HEARTS, Rank.SIX))
        player.hand.add_card(Card(Suit.DIAMONDS, Rank.FIVE))

        assert player.can_double() == True
        assert player.double_bet() == True
        assert player.bet == 200
        assert player.has_doubled == True
        assert player.chips == 800

    def test_player_split(self, player):
        """Test hand splitting creates two hands with equal bets."""
        player.place_bet(100)
        player.hand.add_card(Card(Suit.HEARTS, Rank.EIGHT))
        player.hand.add_card(Card(Suit.DIAMONDS, Rank.EIGHT))

        assert player.can_split() == True
        assert player.split_hand() == True
        assert len(player.split_hands) == 2
        assert player.split_bets == [100, 100]
        assert player.chips == 800

    def test_player_surrender(self, player):
        """Test surrender marks player as surrendered."""
        player.place_bet(100)
        player.hand.add_card(Card(Suit.HEARTS, Rank.EIGHT))
        player.hand.add_card(Card(Suit.DIAMONDS, Rank.NINE))

        assert player.surrender() == True
        assert player.has_surrendered == True

    def test_player_clear_hand(self, player):
        """Test hand clearing resets all hand-related state."""
        player.place_bet(100)
        player.place_insurance()
        player.hand.add_card(Card(Suit.HEARTS, Rank.ACE))

        player.split_hands = [Hand(), Hand()]
        player.split_bets = [100, 100]

        player.clear_hand()
        assert player.hand.cards == []
        assert player.split_hands == []
        assert player.split_bets == []


class TestBot:
    """
    Test cases for the Bot class.

    Test cases:
    - Bot initialization with strategy
    - Safe strategy hitting until 14+
    - Risk taker strategy hitting until 19+
    """

    @pytest.fixture
    def bot(self):
        return Bot("TestBot", StrategyType.SAFE)

    def test_bot_initialization(self, bot):
        """Test bot initialization with name and strategy."""
        assert bot.name == "TestBot"
        assert bot.strategy == StrategyType.SAFE

    def test_bot_play_safe_strategy(self, bot):
        """Test safe strategy hits until score reaches 14 or higher."""
        mock_deck = Mock()
        cards = [Card(Suit.HEARTS, Rank.TWO), Card(Suit.DIAMONDS, Rank.THREE)]
        mock_deck.deal_card.side_effect = cards

        bot.hand.add_card(Card(Suit.SPADES, Rank.TEN))

        with patch("builtins.print"):
            bot.play(mock_deck)

        assert bot.hand.get_score() >= 14
        assert mock_deck.deal_card.call_count > 0

    def test_bot_play_risk_taker_strategy(self):
        """Test risk taker strategy hits until score reaches 19 or higher."""
        bot = Bot("RiskBot", StrategyType.RISK_TAKER)
        mock_deck = Mock()
        cards = [Card(Suit.HEARTS, Rank.TWO)]
        mock_deck.deal_card.side_effect = cards

        bot.hand.add_card(Card(Suit.SPADES, Rank.TEN))
        bot.hand.add_card(Card(Suit.SPADES, Rank.EIGHT))

        with patch("builtins.print"):
            bot.play(mock_deck)

        assert bot.hand.get_score() >= 19
        assert mock_deck.deal_card.call_count > 0


class TestPlayer:
    """
    Test cases for the Player class.

    Test cases:
    - Player stand action maintains hand
    - Player hit action draws additional cards
    """

    @pytest.fixture
    def player(self):
        return Player("TestPlayer")

    def test_player_take_turn_stand(self, player):
        """Test stand action doesn't draw additional cards."""
        mock_deck = Mock()
        dealer_card = Card(Suit.HEARTS, Rank.SEVEN)

        player.hand.add_card(Card(Suit.DIAMONDS, Rank.TEN))
        player.hand.add_card(Card(Suit.CLUBS, Rank.EIGHT))

        with patch("builtins.input", return_value="stand"), patch("builtins.print"):
            player.take_turn(mock_deck, dealer_card)

        assert player.hand.get_score() == 18
        mock_deck.deal_card.assert_not_called()

    def test_player_take_turn_hit(self, player):
        """Test hit action draws one additional card then stands."""
        mock_deck = Mock()
        mock_deck.deal_card.return_value = Card(Suit.HEARTS, Rank.TWO)
        dealer_card = Card(Suit.HEARTS, Rank.SEVEN)

        player.hand.add_card(Card(Suit.DIAMONDS, Rank.TEN))
        player.hand.add_card(Card(Suit.CLUBS, Rank.FIVE))

        with patch("builtins.input", side_effect=["hit", "stand"]), patch(
            "builtins.print"
        ):
            player.take_turn(mock_deck, dealer_card)

        assert player.hand.get_score() == 17
        mock_deck.deal_card.assert_called_once()


class TestGame:
    """
    Test cases for the Game class.

    Test cases:
    - Game initialization with players and bots
    - Player addition to game
    - Initial card dealing
    - Bankrupt player removal
    - Multiple round progression
    - Insurance offering with dealer ace
    - Payout calculation for blackjack
    """

    @pytest.fixture
    def game(self):
        game = Game(max_rounds=2)
        player = Player("TestPlayer")
        game.add_player(player)
        return game

    def test_game_initialization(self, game):
        """Test game initialization with correct player counts and round settings."""
        assert len(game.bots) == 3
        assert len(game.players) == 1
        assert game.current_round == 0
        assert game.max_rounds == 2
        assert game.game_over == False

    def test_add_player(self, game):
        """Test adding new players to the game."""
        new_player = Player("NewPlayer")
        game.add_player(new_player)
        assert len(game.players) == 2
        assert game.players[-1].name == "NewPlayer"

    def test_deal_initial_cards(self, game):
        """Test initial dealing gives 2 cards to all players and dealer."""
        with patch("builtins.print"):
            game.deal_initial_cards()

        for player in game.players + game.bots:
            assert len(player.hand.cards) == 2

        assert len(game.dealer.hand.cards) == 2

    def test_remove_bankrupt_players(self, game):
        """Test removal of players with insufficient chips."""
        game.players[0].chips = 5
        game.remove_bankrupt_players()
        assert len(game.players) == 0

    def test_multiple_rounds(self, game):
        """Test that multiple rounds progress correctly until game over."""
        with patch("builtins.input") as mock_input, patch("builtins.print"):
            mock_input.side_effect = ["100", "n", "stand", "y", "100", "n", "stand"]
            game.start_game()

        assert game.current_round == 2
        assert game.game_over == True

    def test_insurance_offered(self, game):
        """Test insurance is offered when dealer shows ace."""
        game.dealer.hand.add_card(Card(Suit.HEARTS, Rank.ACE))

        with patch("builtins.input", return_value="n"), patch("builtins.print"):
            dealer_card = game.dealer.hand.cards[0]
            if dealer_card.rank == Rank.ACE:
                for player in game.players:
                    insurance = "n"

        assert game.players[0].insurance_bet == 0

    def test_payout_calculations(self, game):
        """Test blackjack payout calculation (3:2 ratio)."""
        player = game.players[0]
        player.place_bet(100)

        player.hand.add_card(Card(Suit.HEARTS, Rank.ACE))
        player.hand.add_card(Card(Suit.DIAMONDS, Rank.KING))

        game.dealer.hand.add_card(Card(Suit.CLUBS, Rank.TEN))
        game.dealer.hand.add_card(Card(Suit.SPADES, Rank.SEVEN))

        with patch("builtins.print"):
            game._process_payout(player, player.hand, 17, False, 100)

        assert player.chips == 1150
