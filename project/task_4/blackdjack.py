import random
from random import randint
from typing import List


class Card:
    def __init__(self, suit: str, rank: str) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self) -> None:
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        return self.cards.pop()


class Hand:
    def __init__(self) -> None:
        self.cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def get_score(self) -> int:
        score = 0
        for card in self.cards:
            if card.rank in ["J", "Q", "K"]:
                score += 10
            elif card.rank == "A":
                if score + 11 <= 21:
                    score += 11
                else:
                    score += 1
            else:
                score += int(card.rank)
        return score


class PlayerBase:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.hand: Hand = Hand()
        self.bet: int = 0

    def place_bet(self, amount: int) -> None:
        self.bet = amount

    def get_hand(self) -> Hand:
        return self.hand


class Bot(PlayerBase):
    def __init__(self, name: str, strategy: str = None) -> None:
        super().__init__(name)
        self.strategy: str = strategy

    def optional_strategy(self, deck: Deck) -> None:
        while self.hand.get_score() < 17:
            self.hand.add_card(deck.deal_card())

    def cowardly_strategy(self, deck: Deck) -> None:
        while self.hand.get_score() < 12:
            self.hand.add_card(deck.deal_card())

    def play(self, deck: Deck) -> None:
        if self.strategy == "optional":
            self.optional_strategy(deck)
        elif self.strategy == "cowardly":
            self.cowardly_strategy(deck)


class Player(PlayerBase):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def take_turn(self, deck: Deck) -> None:
        while self.hand.get_score() < 21:
            print(
                f"\n{self.name}'s hand: {', '.join(str(card) for card in self.hand.cards)}"
            )
            action = input(
                "Choose an action (hit/stand/double/triple/insure): "
            ).lower()

            if action == "hit":
                self.hand.add_card(deck.deal_card())
            elif action == "stand":
                break
            elif action == "double" and len(self.hand.cards) == 2:
                self.place_bet(self.bet * 2)
                self.hand.add_card(deck.deal_card())
                break
            elif action == "triple" and len(self.hand.cards) == 2:
                self.place_bet(self.bet * 3)
                self.hand.add_card(deck.deal_card())
                break
            elif action == "insure" and self.hand.cards[0].rank == "A":
                insurance_bet = int(input("Enter insurance bet amount: "))
                self.place_bet(insurance_bet)
                break
            else:
                print(
                    "Invalid action. Please choose 'hit', 'stand', 'double', 'triple', or 'insure'."
                )


class Game:
    def __init__(self) -> None:
        self.deck: Deck = Deck()
        self.bots: List[Bot] = [Bot("Bot 1", "optional"), Bot("Bot 2", "cowardly")]
        self.dealer: Bot = Bot("Dealer")
        self.players: List[Player] = []
        self.round_winner: str = None

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def place_bets(self) -> None:
        for player in self.players:
            bet = int(input(f"{player.name}, your bet: "))
            player.place_bet(bet)

        for bot in self.bots:
            bet = randint(10, 100)
            bot.place_bet(bet)

    def play_round(self) -> None:
        for bot in self.bots:
            bot.hand.add_card(self.deck.deal_card())
            bot.hand.add_card(self.deck.deal_card())

        for player in self.players:
            player.hand.add_card(self.deck.deal_card())
            player.hand.add_card(self.deck.deal_card())

        self.dealer.hand.add_card(self.deck.deal_card())
        self.dealer.hand.add_card(self.deck.deal_card())

        for bot in self.bots:
            print(
                f"{bot.name}'s hand: {', '.join(str(card) for card in bot.hand.cards)}"
            )
        for player in self.players:
            print(
                f"{player.name}'s hand: {', '.join(str(card) for card in player.hand.cards)}"
            )

        for player in self.players:
            player.take_turn(self.deck)

        for bot in self.bots:
            bot.play(self.deck)

        # Ход дилера
        print(
            f"\nDealer's hand: {', '.join(str(card) for card in self.dealer.hand.cards)}"
        )
        while self.dealer.hand.get_score() < 17:
            print(
                f"Dealer hits: {str(self.dealer.hand.cards[-1])}"
            )  # Показываем какую карту дилер берет
            self.dealer.hand.add_card(self.deck.deal_card())

        self.determine_winner()

    def determine_winner(self) -> None:
        dealer_score = self.dealer.hand.get_score()
        print(f"Dealer's score: {dealer_score}")

        for player in self.players:
            player_score = player.hand.get_score()
            print(f"{player.name}'s score: {player_score}")

            if player_score > 21:
                print(f"{player.name} busts!")
                self.round_winner = "Dealer"
            elif dealer_score > 21 or player_score > dealer_score:
                print(f"{player.name} wins!")
                self.round_winner = player.name
            elif player_score == dealer_score:
                print(f"{player.name} ties with Dealer!")
                self.round_winner = "Tie"
            else:
                print(f"Dealer wins over {player.name}")
                self.round_winner = "Dealer"

    def show_results(self) -> None:
        print(f"Winner of the round: {self.round_winner}")

    def start_game(self) -> None:
        self.place_bets()
        self.play_round()
        self.show_results()
