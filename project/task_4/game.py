from typing import List
from project.task_4.core import Deck, Hand, Card
from project.task_4.players import PlayerBase, Player, Bot
from project.task_4.enums import Rank, StrategyType


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
        self.bots: List[Bot] = [
            Bot("Safe Bot", StrategyType.SAFE),
            Bot("Risk Taker Bot", StrategyType.RISK_TAKER),
            Bot("Unpredictable Bot", StrategyType.UNPREDICTABLE),
        ]
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
            bet = bot.calculate_bet()
            if bot.chips < 10:  # Minimum bet check
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

        if dealer_up_card.rank == Rank.ACE:
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

        self.remove_bankrupt_players()

        for player in self.players + self.bots + [self.dealer]:
            player.bet = 0
            player.insurance_bet = 0
            player.has_doubled = False
            player.has_surrendered = False

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

        if hand.is_five_card_charlie():
            print(f"{player.name}{split_text}: five card charlie - win")
        elif hand.is_busted():
            print(f"{player.name}{split_text}: bust - lose")
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
                refund = player.bet // 2
                player.chips += refund
                continue

            if dealer_blackjack and player.insurance_bet > 0:
                insurance_winnings = player.insurance_bet * 3
                player.chips += insurance_winnings

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
            pass
        elif hand.is_five_card_charlie():
            player.chips += bet * 2
        elif dealer_blackjack:
            if hand.is_blackjack():
                player.chips += bet
        elif hand.is_blackjack():
            winnings = int(bet * 1.5)
            total_win = bet + winnings
            player.chips += total_win
        elif dealer_score > 21:
            player.chips += bet * 2
        elif hand.get_score() > dealer_score:
            player.chips += bet * 2
        elif hand.get_score() == dealer_score:
            player.chips += bet

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
