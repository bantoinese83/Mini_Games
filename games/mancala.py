import random
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError


class Mancala:
    def __init__(self, seed_count=4, pit_count=6):
        self.seed_count = seed_count
        self.pit_count = pit_count
        self.board = [seed_count] * (pit_count * 2)  # Initialize the board with seeds in each pit
        self.player_turn = random.choice([0, 1])  # Randomly select the starting player
        self.mancalas = [pit_count * seed_count] * 2  # Initialize the Mancalas with zero seeds
        self.game_over = False

    def print_board(self):
        print("Player B: ", self.board[:self.pit_count][::-1])  # Print Player B's pits in reverse order
        print("Player A: ", self.board[self.pit_count:])  # Print Player A's pits
        print("Mancala A: ", self.mancalas[0], "   Mancala B: ", self.mancalas[1])  # Print both players' Mancalas

    def move(self, pit):
        if not self.is_valid_move(pit):
            print("Invalid move! Please choose a non-empty pit from your side.")
            return

        seeds = self.board[pit + self.player_turn * self.pit_count]
        self.board[pit + self.player_turn * self.pit_count] = 0

        index = pit + 1
        while seeds:
            if self.player_turn == 0 and index == self.pit_count * 2:
                index = 0
            elif self.player_turn == 1 and index == self.pit_count:
                index = self.pit_count + 1

            # Skip opponent's Mancala
            if index != self.player_turn * self.pit_count:
                self.board[index] += 1
                seeds -= 1
            index = (index + 1) % (self.pit_count * 2)

        self.check_capture(index - 1)
        self.switch_player_turn()
        self.check_game_over()

    def is_valid_move(self, pit):
        return 0 <= pit < self.pit_count and self.board[pit + self.player_turn * self.pit_count] > 0

    def check_capture(self, pit):
        if pit != self.player_turn * self.pit_count and self.board[pit] == 1:
            opposite_pit = self.pit_count * 2 - pit - 1
            if self.board[opposite_pit] > 0:
                self.mancalas[self.player_turn] += self.board[pit] + self.board[opposite_pit]
                self.board[pit] = 0
                self.board[opposite_pit] = 0

    def switch_player_turn(self):
        if self.game_over:
            return
        if self.player_turn == 0:
            self.player_turn = 1
        else:
            self.player_turn = 0

    def check_game_over(self):
        player_a_pits_empty = all(seeds == 0 for seeds in self.board[:self.pit_count])
        player_b_pits_empty = all(seeds == 0 for seeds in self.board[self.pit_count:])
        if player_a_pits_empty or player_b_pits_empty:
            self.game_over = True

    def get_winner(self):
        if self.mancalas[0] > self.mancalas[1]:
            return "Player A wins!"
        elif self.mancalas[0] < self.mancalas[1]:
            return "Player B wins!"
        else:
            return "It's a tie!"

    def play(self):
        while not self.game_over:
            self.print_board()
            print(f"Player {chr(ord('A') + self.player_turn)}'s turn")
            try:
                pit = prompt("Choose a pit (0-5): ", validator=PitValidator())
                self.move(int(pit))
            except ValidationError as e:
                print(f"Error: {e}")
            except ValueError:
                print("Invalid input! Please enter a valid integer between 0 and 5.")

        print(self.get_winner())


class PitValidator(Validator):
    def validate(self, document):
        value = document.text
        try:
            pit = int(value)
            if not 0 <= pit <= 5:
                raise ValidationError(message="Pit number must be between 0 and 5.", cursor_position=len(value))
        except ValueError:
            raise ValidationError(message="Invalid input. Please enter a valid integer.", cursor_position=len(value))


def play():
    game = Mancala(seed_count=4, pit_count=6)
    game.play()
