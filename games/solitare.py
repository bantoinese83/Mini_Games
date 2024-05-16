import random

import emoji
from rich.console import Console
from rich.table import Table


class Solitaire:
    SUITS = [emoji.emojize(':hearts:'), emoji.emojize(':diamonds:'), emoji.emojize(':clubs:'),
             emoji.emojize(':spades:')]
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.deck = [(rank, suit) for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(self.deck)
        self.tableau = [[] for _ in range(7)]
        self.foundation = {suit: [] for suit in self.SUITS}
        self.stock = self.deck[:28]
        self.waste = self.deck[28:]
        self.deal_cards()

    def deal_cards(self):
        for i in range(7):
            for j in range(i + 1):
                self.tableau[i].append(self.stock.pop(0))
                if j == i:
                    self.tableau[i][j] = (self.tableau[i][j][0], self.tableau[i][j][1], True)

    def move_card(self, command):
        if command == 'd':
            if len(self.stock) == 0:
                self.stock = self.waste
                self.waste = []
            else:
                self.waste.append(self.stock.pop(0))
        elif command == 'm':
            source = input("Enter source card (row, column): ").strip().split(',')
            dest = input("Enter destination card (row, column): ").strip().split(',')
            source_row, source_col = int(source[0]), int(source[1])
            dest_row, dest_col = int(dest[0]), int(dest[1])
            source_card = self.tableau[source_row][source_col]
            dest_card = self.tableau[dest_row][dest_col]
            if source_card[2] and not dest_card[2]:
                if self.is_valid_move(source_card, dest_card):
                    self.tableau[dest_row][dest_col] = source_card
                    self.tableau[source_row][source_col] = (source_card[0], source_card[1], False)
                else:
                    print("Invalid move!")
            else:
                print("Invalid move!")
        else:
            print("Invalid command!")

    def print_board(self):
        console = Console()
        for i, row in enumerate(self.tableau, start=1):
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Card")
            for card in row:
                table.add_row(str(card))
            console.print(f"Row {i}:")
            console.print(table)
        console.print("Stock:")
        console.print(self.stock)
        console.print("Waste:")
        console.print(self.waste)
        console.print("Foundation:")
        for suit in self.SUITS:
            console.print(f"{suit}: {self.foundation[suit]}")
        print("\nCommands: (D)eal, (M)ove, (Q)uit")

    def play(self):
        while True:
            self.print_board()
            command = input("Enter a command: ").strip().lower()
            if command == 'q':
                print("Thanks for playing!")
                break
            else:
                self.move_card(command)

    @staticmethod
    def is_valid_move(source_card, dest_card):
        if source_card[0] == 'King':
            return dest_card[0] == 'Ace' and source_card[1] != dest_card[1]
        elif source_card[0] == 'Queen':
            return dest_card[0] == 'King' and source_card[1] != dest_card[1]
        elif source_card[0] == 'Jack':
            return dest_card[0] == 'Queen' and source_card[1] != dest_card[1]
        elif source_card[0] == '10':
            return dest_card[0] == 'Jack' and source_card[1] != dest_card[1]
        elif source_card[0] == '9':
            return dest_card[0] == '10' and source_card[1] != dest_card[1]
        elif source_card[0] == '8':
            return dest_card[0] == '9' and source_card[1] != dest_card[1]
        elif source_card[0] == '7':
            return dest_card[0] == '8' and source_card[1] != dest_card[1]
        elif source_card[0] == '6':
            return dest_card[0] == '7' and source_card[1] != dest_card[1]
        elif source_card[0] == '5':
            return dest_card[0] == '6' and source_card[1] != dest_card[1]
        elif source_card[0] == '4':
            return dest_card[0] == '5' and source_card[1] != dest_card[1]
        elif source_card[0] == '3':
            return dest_card[0] == '4' and source_card[1] != dest_card[1]
        elif source_card[0] == '2':
            return dest_card[0] == '3' and source_card[1] != dest_card[1]
        elif source_card[0] == 'Ace':
            return dest_card[0] == '2' and source_card[1] != dest_card[1]
        else:
            return False


def play():
    game = Solitaire()
    game.play()
