import random
from typing import List, Optional


class Card:
    """
    Represents a playing card with suit and rank

    Attributes:
        suit (str): The suit of the card (Hearts, Diamonds, Clubs, Spades)
        rank (str): The rank of the card (2-10, J, Q, K, A)
    """

    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def get_value(self) -> int:
        """
        Get the numerical value of the card

        Returns:
            int: Value of the card (2-10, 10 for face cards, 11 for Ace)
        """
        if self.rank in ["J", "Q", "K"]:
            return 10
        elif self.rank == "A":
            return 11
        else:
            return int(self.rank)

    def is_same_rank(self, other_card: "Card") -> bool:
        """
        Check if two cards have the same rank

        Parameters:
            other_card (Card): Another card to compare with

        Returns:
            bool: True if cards have same rank, False otherwise
        """
        rank_values = {"J": "10", "Q": "10", "K": "10", "A": "A"}
        rank1 = rank_values.get(self.rank, self.rank)
        rank2 = rank_values.get(other_card.rank, other_card.rank)
        return rank1 == rank2


class Deck:
    """
    Represents a deck of 52 playing cards

    Attributes:
        cards (List[Card]): List of cards in the deck
    """

    def __init__(self) -> None:
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
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
            if card.rank == "A":
                aces += 1
                score += 11
            elif card.rank in ["J", "Q", "K"]:
                score += 10
            else:
                score += int(card.rank)

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
            return True
        return False

    def place_insurance(self) -> bool:
        """
        Place an insurance bet (half of original bet)

        Returns:
            bool: True if insurance was placed successfully, False otherwise
        """
        insurance_amount = self.bet // 2
        if insurance_amount <= (self.chips - self.bet):
            self.insurance_bet = insurance_amount
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
            self.bet *= 2
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
        strategy (str): Bot's playing strategy ('optional' or 'cowardly')
    """

    def __init__(self, name: str, strategy: Optional[str] = None) -> None:
        """
        Initialize a bot player

        Parameters:
            name (str): Bot's name
            strategy (Optional[str]): Playing strategy ('optional' or 'cowardly')
        """
        super().__init__(name)
        self.strategy: Optional[str] = strategy

    def optional_strategy(self, deck: Deck) -> None:
        """
        Optional strategy: hit until score reaches 17

        Parameters:
            deck (Deck): Deck to draw cards from
        """
        while self.hand.get_score() < 17:
            self.hand.add_card(deck.deal_card())

    def cowardly_strategy(self, deck: Deck) -> None:
        """
        Cowardly strategy: hit until score reaches 12

        Parameters:
            deck (Deck): Deck to draw cards from
        """
        while self.hand.get_score() < 12:
            self.hand.add_card(deck.deal_card())

    def play(self, deck: Deck) -> None:
        """
        Execute bot's playing strategy

        Parameters:
            deck (Deck): Deck to draw cards from
        """
        if self.strategy == "optional":
            self.optional_strategy(deck)
        elif self.strategy == "cowardly":
            self.cowardly_strategy(deck)


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
        current_bet = self.split_bets[0] if is_split and self.split_bets else self.bet

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


class Game:
    """
    Main game controller for Blackjack

    Attributes:
        deck (Deck): Game deck
        bots (List[Bot]): List of AI players
        dealer (Bot): Dealer player
        players (List[Player]): List of human players
        current_round (int): Current round number
        max_rounds (int): Maximum number of rounds
        game_over (bool): Whether game has ended
    """

    def __init__(self, max_rounds: int = 5) -> None:
        """
        Initialize a new Blackjack game

        Parameters:
            max_rounds (int): Maximum number of rounds to play
        """
        self.deck: Deck = Deck()
        self.bots: List[Bot] = [Bot("Bot 1", "optional"), Bot("Bot 2", "cowardly")]
        self.dealer: Bot = Bot("Dealer")
        self.players: List[Player] = []
        self.current_round: int = 0
        self.max_rounds: int = max_rounds
        self.game_over: bool = False

    def add_player(self, player: Player) -> None:
        """
        Add a human player to the game

        Parameters:
            player (Player): Player to add
        """
        self.players.append(player)

    def place_bets(self) -> None:
        """Collect bets from all players and bots"""
        print("Placing bets:")
        for player in self.players:
            while True:
                try:
                    bet = int(input(f"{player.name} bet (chips: {player.chips}): "))
                    if player.place_bet(bet):
                        break
                    else:
                        print(f"Invalid bet! You have {player.chips} chips.")
                except ValueError:
                    print("Please enter a valid number")

        for bot in self.bots:
            bet = max(10, min(100, bot.chips // 10))
            if bot.chips < 10:
                bet = bot.chips
            if bot.place_bet(bet):
                print(f"{bot.name} bets {bet}")

    def deal_initial_cards(self) -> None:
        """Deal initial two cards to all players and dealer"""
        for _ in range(2):
            for bot in self.bots:
                bot.hand.add_card(self.deck.deal_card())
            for player in self.players:
                player.hand.add_card(self.deck.deal_card())
            self.dealer.hand.add_card(self.deck.deal_card())

    def play_round(self) -> None:
        """Play one complete round of Blackjack"""
        self.current_round += 1
        print(f"\nRound {self.current_round}")

        self.place_bets()

        for player in self.players + self.bots + [self.dealer]:
            player.clear_hand()

        self.deal_initial_cards()

        dealer_up_card = self.dealer.hand.cards[0]
        print(f"Dealer shows: {dealer_up_card}")

        if dealer_up_card.rank == "A":
            for player in self.players:
                insurance = input(f"{player.name} - insurance? (y/n): ").lower()
                if insurance == "y":
                    player.place_insurance()

        for player in self.players:
            player.take_turn(self.deck, dealer_up_card)

        for bot in self.bots:
            bot.play(self.deck)

        print(f"Dealer: {[str(card) for card in self.dealer.hand.cards]}")
        while self.dealer.hand.get_score() < 17:
            card = self.deck.deal_card()
            self.dealer.hand.add_card(card)
            print(f"Dealer hits: {card}")

        dealer_score = self.dealer.hand.get_score()
        dealer_blackjack = self.dealer.hand.is_blackjack()

        print(f"Dealer score: {dealer_score}")

        for player in self.players + self.bots:
            if player.split_hands:
                for i, split_hand in enumerate(player.split_hands):
                    self._process_player_result(
                        player, split_hand, dealer_score, dealer_blackjack, i
                    )
            else:
                self._process_player_result(
                    player, player.hand, dealer_score, dealer_blackjack
                )

        self.update_chips()

        for player in self.players + self.bots + [self.dealer]:
            player.bet = 0
            player.insurance_bet = 0
            player.has_doubled = False
            player.has_surrendered = False

        self.remove_bankrupt_players()

        if (
            self.current_round >= self.max_rounds
            or len(self.players + self.bots) == 0
            or self.deck.cards_remaining() < 10
        ):
            self.game_over = True

    def _process_player_result(
        self,
        player: PlayerBase,
        hand: Hand,
        dealer_score: int,
        dealer_blackjack: bool,
        split_index: int = -1,
    ) -> None:
        """
        Process and display result for a player's hand

        Parameters:
            player (PlayerBase): Player whose hand is being evaluated
            hand (Hand): Hand to evaluate
            dealer_score (int): Dealer's final score
            dealer_blackjack (bool): Whether dealer has blackjack
            split_index (int): Index of split hand (-1 for main hand)
        """
        split_text = f" (split {split_index + 1})" if split_index >= 0 else ""

        if player.has_surrendered:
            print(f"{player.name}{split_text}: surrendered")
            return

        player_score = hand.get_score()

        print(f"{player.name}{split_text}: {player_score}")

        if hand.is_busted():
            print(f"{player.name}{split_text}: bust - lose")
        elif hand.is_five_card_charlie():
            print(f"{player.name}{split_text}: five card charlie - win")
        elif dealer_blackjack and hand.is_blackjack():
            print(f"{player.name}{split_text}: push - both blackjack")
        elif dealer_blackjack:
            print(f"{player.name}{split_text}: lose - dealer blackjack")
        elif hand.is_blackjack():
            print(f"{player.name}{split_text}: blackjack - win 3:2")
        elif dealer_score > 21:
            print(f"{player.name}{split_text}: win - dealer bust")
        elif player_score > dealer_score:
            print(f"{player.name}{split_text}: win")
        elif player_score == dealer_score:
            print(f"{player.name}{split_text}: push")
        else:
            print(f"{player.name}{split_text}: lose")

        if dealer_blackjack and player.insurance_bet > 0:
            print(f"{player.name}: insurance pays 2:1")

    def update_chips(self) -> None:
        """Update chip counts based on round results"""
        dealer_score = self.dealer.hand.get_score()
        dealer_blackjack = self.dealer.hand.is_blackjack()

        for player in self.players + self.bots:
            if player.has_surrendered:
                player.chips -= player.bet // 2
                continue

            if player.split_hands:
                for i, split_hand in enumerate(player.split_hands):
                    bet = (
                        player.split_bets[i]
                        if i < len(player.split_bets)
                        else player.bet
                    )
                    self._process_payout(
                        player, split_hand, dealer_score, dealer_blackjack, bet
                    )
            else:
                self._process_payout(
                    player, player.hand, dealer_score, dealer_blackjack, player.bet
                )

            if dealer_blackjack and player.insurance_bet > 0:
                player.chips += player.insurance_bet * 2
                print(f"{player.name} wins insurance: {player.insurance_bet * 2}")

    def _process_payout(
        self,
        player: PlayerBase,
        hand: Hand,
        dealer_score: int,
        dealer_blackjack: bool,
        bet: int,
    ) -> None:
        """
        Process payout for a specific hand

        Parameters:
            player (PlayerBase): Player to receive payout
            hand (Hand): Hand being evaluated
            dealer_score (int): Dealer's final score
            dealer_blackjack (bool): Whether dealer has blackjack
            bet (int): Bet amount for this hand
        """
        if hand.is_busted():
            player.chips -= bet
            print(f"{player.name} loses {bet} chips (bust)")
        elif hand.is_five_card_charlie():
            player.chips += bet
            print(f"{player.name} wins {bet} chips (five card charlie)")
        elif dealer_blackjack:
            if hand.is_blackjack():
                print(f"{player.name} pushes (both blackjack)")
            else:
                player.chips -= bet
                print(f"{player.name} loses {bet} chips (dealer blackjack)")
        elif hand.is_blackjack():
            winnings = int(bet * 1.5)
            player.chips += winnings
            print(f"{player.name} wins {winnings} chips (blackjack 3:2)")
        elif dealer_score > 21:
            player.chips += bet
            print(f"{player.name} wins {bet} chips (dealer bust)")
        elif hand.get_score() > dealer_score:
            player.chips += bet
            print(f"{player.name} wins {bet} chips (higher score)")
        elif hand.get_score() == dealer_score:
            print(f"{player.name} pushes (same score)")
        else:
            player.chips -= bet
            print(f"{player.name} loses {bet} chips (lower score)")

    def remove_bankrupt_players(self) -> None:
        """Remove players with insufficient chips"""
        self.players = [p for p in self.players if p.chips >= 10]
        self.bots = [b for b in self.bots if b.chips >= 10]

    def show_results(self) -> None:
        """Display current chip counts for all players"""
        print("\nChip counts:")
        for player in self.players + self.bots:
            print(f"{player.name}: {player.chips}")

    def start_game(self) -> None:
        """Start and run the main game loop"""
        print("Welcome to Blackjack!")
        print(f"Game will run for {self.max_rounds} rounds")

        while not self.game_over and self.current_round < self.max_rounds:
            self.play_round()
            self.show_results()

            if not self.game_over and self.current_round < self.max_rounds:
                cont = input("\nContinue to next round? (y/n): ").lower()
                if cont != "y":
                    break

            if self.deck.cards_remaining() < 10:
                print("Shuffling new deck...")
                self.deck = Deck()

        print(f"\nFinal winner: {self.get_final_winner()}")

    def get_final_winner(self) -> str:
        """
        Determine the final winner of the game

        Returns:
            str: Name and chips of the winner
        """
        all_players = self.players + self.bots
        if not all_players:
            return "No winners"

        winner = max(all_players, key=lambda p: p.chips)
        return f"{winner.name} with {winner.chips} chips"
