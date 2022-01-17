import random

class Card:
    """French playing cards.

    Class attributes:
    suit_names -- the four suits Clubs, Diamonds, Hearts, Spades
    rank_names -- the 13 ranks in each suit: Two--Ten, Jack, Queen, King, Ace

    Data attributes:
    suit, rank -- the Card's suit and rank, as indices into the lists above
    """

    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
             'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank_names[self.rank]} of {self.suit_names[self.suit]}"

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit
    
    def __gt__(self, other):
        return (self.rank > other.rank) or (self.rank == other.rank and self.suit > other.suit)

class Deck:
    """ A deck of cards.

    Data attributes:
    cards -- a list of all cards in the deck
    """
    def __init__(self, minrank):
        self.cards = []
        for j in range(4):
            for i in range(minrank, 13):
                self.cards.append(Card(j,i))

    def __str__(self):
        list = [str(x) for x in self.cards]
        return ', '.join(list)

    def pop(self):
        """Remove and return last card from deck."""
        return self.cards.pop()

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

class Player:
    """A player of the card game.

    Data attributes:
    name -- the name of the player
    cards -- a list of all the player's cards (their "hand")
    """
    def __init__(self, name):
        self.name = name
        self.cards = []

    def __str__(self):
        print_cards = " no cards" if len(self.cards) == 0 else ': '+ ', '.join([str(x) for x in self.cards])
        return f"Player {self.name} has{print_cards}"

    def add_card(self, card):
        """Add card to this player's hand."""
        self.cards.append(card)

    def num_cards(self):
        """Return the number of cards in this player's hand."""
        return len(self.cards)

    def remove_card(self):
        """Remove the first card from this player's hand and return it."""
        return self.cards.pop(0)

class CardGame:
    """A class for playing card games.

    Data attributes:
    players -- a list of Player objects which participate in the game
    deck -- a Deck of Cards used for playing
    numcards -- the number of Cards in the game
    """
    def __init__(self, player_names, minrank):
        self.deck = Deck(minrank)
        self.numcards = len(self.deck.cards)
        self.players = []
        for name in player_names:
            self.players.append(Player(name))

    def __str__(self):
        list = []
        for player in self.players:
            list.append(str(player))

        return '\n'.join(list)

    def shuffle_deck(self):
        """Shuffle this game's deck."""
        self.deck.shuffle()

    def deal_cards(self):
        """Deal all of the cards in the deck to the players, round-robin."""
        current_player = 0
        while len(self.deck.cards) > 0:
            self.players[current_player].add_card(self.deck.pop())
            current_player += 1
            current_player %= len(self.players)

    def simple_turn(self):
        """Play a very simple game.
        For each player, play the first card.
        The winner is the player with the highest cards.
        """
        current_maximum = Card(0,0)
        max_name = -1
        played_cards = []
        for player in self.players:
            if not player.cards:
                continue
            played_card = player.remove_card()
            played_cards.append(played_card)
            print(f"Player {player.name}: {played_card}")
            if max_name == -1 or played_card > current_maximum:
                current_maximum = played_card
                max_name = player.name

        return (max_name, played_cards)

    def play_simple(self):
        while True:
            for player in self.players:
                if len(player.cards) == self.numcards:
                    return player.name
            (name, cards) = self.simple_turn()
            random.shuffle(cards) 

            for i in range(len(self.players)):
                if self.players[i].name == name:
                    for card in cards:
                        self.players[i].add_card(card)





