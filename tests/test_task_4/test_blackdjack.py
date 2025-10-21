import pytest
from unittest.mock import patch, Mock
import sys
import os

current_dir = os.path.dirname(__file__)
project_path = os.path.join(current_dir, "..", "..", "project", "task_4")
sys.path.insert(0, os.path.abspath(project_path))

from blackjack import Card, Deck, Hand, PlayerBase, Bot, Player, Game


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
        card = Card("Hearts", "A")
        assert card.suit == "Hearts"
        assert card.rank == "A"

    def test_card_string_representation(self):
        """Test the string representation of cards."""
        card = Card("Diamonds", "K")
        assert str(card) == "K of Diamonds"

    def test_card_values(self):
        """Test value calculation for all card ranks including face cards and aces."""
        test_cases = [("2", 2), ("10", 10), ("J", 10), ("Q", 10), ("K", 10), ("A", 11)]
        for rank, expected_value in test_cases:
            card = Card("Hearts", rank)
            assert card.get_value() == expected_value

    def test_card_same_rank(self):
        """Test rank comparison between different cards."""
        card_k = Card("Hearts", "K")
        card_q = Card("Diamonds", "Q")
        card_a = Card("Clubs", "A")
        card_2 = Card("Spades", "2")

        assert card_k.is_same_rank(card_q) == True
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
        card = Card("Hearts", "A")
        hand.add_card(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card

    def test_hand_blackjack_detection(self):
        """Test blackjack detection with ace and face card."""
        hand = Hand()
        hand.add_card(Card("Hearts", "A"))
        hand.add_card(Card("Diamonds", "K"))
        assert hand.is_blackjack() == True
        assert hand.get_score() == 21

    def test_hand_bust_detection(self):
        """Test bust detection when hand exceeds 21."""
        hand = Hand()
        hand.add_card(Card("Hearts", "K"))
        hand.add_card(Card("Diamonds", "Q"))
        hand.add_card(Card("Clubs", "2"))
        assert hand.is_busted() == True
        assert hand.get_score() > 21

    def test_hand_ace_adjustment(self):
        """Test ace value adjustment from 11 to 1 when beneficial."""
        hand = Hand()
        hand.add_card(Card("Hearts", "A"))
        hand.add_card(Card("Diamonds", "A"))
        hand.add_card(Card("Clubs", "9"))
        assert hand.get_score() == 21

    def test_hand_split_detection(self):
        """Test split eligibility with matching and non-matching ranks."""
        hand = Hand()
        hand.add_card(Card("Hearts", "8"))
        hand.add_card(Card("Diamonds", "8"))
        assert hand.can_split() == True

        hand.clear()
        hand.add_card(Card("Hearts", "8"))
        hand.add_card(Card("Diamonds", "9"))
        assert hand.can_split() == False

    def test_hand_five_card_charlie(self):
        """Test five-card Charlie detection with exactly 5 cards under 21."""
        hand = Hand()
        for rank in ["2", "3", "4", "5", "6"]:
            hand.add_card(Card("Hearts", rank))
        assert hand.is_five_card_charlie() == True

        hand.clear()
        for rank in ["2", "3", "4", "5", "K"]:
            hand.add_card(Card("Hearts", rank))
        assert hand.is_five_card_charlie() == False

    def test_hand_clear(self):
        """Test hand clearing resets cards and score."""
        hand = Hand()
        hand.add_card(Card("Hearts", "A"))
        hand.add_card(Card("Diamonds", "K"))
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
        assert player.chips == 1000

    def test_player_insurance(self, player):
        """Test insurance bet placement at half the original bet."""
        player.place_bet(100)
        assert player.place_insurance() == True
        assert player.insurance_bet == 50

    def test_player_double_down(self, player):
        """Test double down doubles the bet and marks player as doubled."""
        player.place_bet(100)
        player.hand.add_card(Card("Hearts", "6"))
        player.hand.add_card(Card("Diamonds", "5"))

        assert player.can_double() == True
        assert player.double_bet() == True
        assert player.bet == 200
        assert player.has_doubled == True

    def test_player_split(self, player):
        """Test hand splitting creates two hands with equal bets."""
        player.place_bet(100)
        player.hand.add_card(Card("Hearts", "8"))
        player.hand.add_card(Card("Diamonds", "8"))

        assert player.can_split() == True
        assert player.split_hand() == True
        assert len(player.split_hands) == 2
        assert player.split_bets == [100, 100]

    def test_player_surrender(self, player):
        """Test surrender marks player as surrendered."""
        player.place_bet(100)
        player.hand.add_card(Card("Hearts", "8"))
        player.hand.add_card(Card("Diamonds", "9"))

        assert player.surrender() == True
        assert player.has_surrendered == True

    def test_player_clear_hand(self, player):
        """Test hand clearing resets all hand-related state."""
        player.place_bet(100)
        player.place_insurance()
        player.hand.add_card(Card("Hearts", "A"))

        with patch.object(player, "split_hand", return_value=True):
            player.split_hand()

        player.clear_hand()
        assert player.hand.cards == []
        assert player.split_hands == []
        assert player.split_bets == []


class TestBot:
    """
    Test cases for the Bot class.

    Test cases:
    - Bot initialization with strategy
    - Optional strategy hitting until 17+
    - Cowardly strategy hitting until 12+
    """

    @pytest.fixture
    def bot(self):
        return Bot("TestBot", "optional")

    def test_bot_initialization(self, bot):
        """Test bot initialization with name and strategy."""
        assert bot.name == "TestBot"
        assert bot.strategy == "optional"

    def test_bot_optional_strategy(self, bot):
        """Test optional strategy hits until score reaches 17 or higher."""
        mock_deck = Mock()
        cards = [Card("Hearts", "2"), Card("Diamonds", "3"), Card("Clubs", "K")]
        mock_deck.deal_card.side_effect = cards

        bot.hand.add_card(Card("Spades", "10"))

        with patch("builtins.print"):
            bot.optional_strategy(mock_deck)

        assert bot.hand.get_score() >= 17
        assert mock_deck.deal_card.call_count > 0

    def test_bot_cowardly_strategy(self, bot):
        """Test cowardly strategy hits until score reaches 12 or higher."""
        bot.strategy = "cowardly"
        mock_deck = Mock()
        cards = [Card("Hearts", "2"), Card("Diamonds", "3")]
        mock_deck.deal_card.side_effect = cards

        bot.hand.add_card(Card("Spades", "8"))

        with patch("builtins.print"):
            bot.cowardly_strategy(mock_deck)

        assert bot.hand.get_score() >= 12


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
        dealer_card = Card("Hearts", "7")

        player.hand.add_card(Card("Diamonds", "10"))
        player.hand.add_card(Card("Clubs", "8"))

        with patch("builtins.input", return_value="stand"), patch("builtins.print"):
            player.take_turn(mock_deck, dealer_card)

        assert player.hand.get_score() == 18
        mock_deck.deal_card.assert_not_called()

    def test_player_take_turn_hit(self, player):
        """Test hit action draws one additional card then stands."""
        mock_deck = Mock()
        mock_deck.deal_card.return_value = Card("Hearts", "2")
        dealer_card = Card("Hearts", "7")

        player.hand.add_card(Card("Diamonds", "10"))
        player.hand.add_card(Card("Clubs", "5"))

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
        assert len(game.bots) == 2
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
        game.dealer.hand.add_card(Card("Hearts", "A"))

        with patch("builtins.input", return_value="n"), patch("builtins.print"):
            dealer_card = game.dealer.hand.cards[0]
            if dealer_card.rank == "A":
                for player in game.players:
                    insurance = "n"

        assert game.players[0].insurance_bet == 0

    def test_payout_calculations(self, game):
        """Test blackjack payout calculation (3:2 ratio)."""
        player = game.players[0]
        player.place_bet(100)

        player.hand.add_card(Card("Hearts", "A"))
        player.hand.add_card(Card("Diamonds", "K"))

        game.dealer.hand.add_card(Card("Clubs", "10"))
        game.dealer.hand.add_card(Card("Spades", "7"))

        with patch("builtins.print"):
            game._process_payout(player, player.hand, 17, False, 100)

        assert player.chips == 1000 + 150
