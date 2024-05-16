import os
import time
import random


class ConnectFour:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.current_player = '🔴'
        self.move_history = []
        self.first_turn_player = '🔴'  # Track who starts the game

    @staticmethod
    def clear_screen():
        # Clear the console screen in a cross-platform way
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_board(self):
        self.clear_screen()

        # Determine the width of each cell dynamically based on the length of the longest chip
        cell_width = max(len(cell) for row in self.board for cell in row) + 2

        # Construct the horizontal border
        horizontal_line = '+'.join(['-' * (cell_width * 7 + 3)] * 2)

        # Print the top border
        print(horizontal_line)

        # Print each row with chips enclosed in boxes
        for row in range(5, -1, -1):
            for col in range(7):
                print('|', end='')
                print(f' {self.board[row][col].center(cell_width)} ', end='')
            print('|')
            print(horizontal_line)

        # Print column numbers at the bottom
        print('  ' + '   '.join(map(str, range(1, 8))))

    def is_valid_move(self, col):
        return self.board[-1][col] == ' '

    def make_move(self, col):
        for row in self.board:
            if row[col] == ' ':
                row[col] = self.current_player
                self.move_history.append(col)
                break

    def undo_move(self):
        if self.move_history:
            last_col = self.move_history.pop()
            for row in reversed(self.board):
                if row[last_col] != ' ':
                    row[last_col] = ' '
                    break
            self.switch_player()
        else:
            print("No moves to undo!")

    def check_win(self):
        # Check all possible win conditions
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == self.current_player:
                    if (self.check_line(row, col, 1, 0) or  # Vertical
                            self.check_line(row, col, 0, 1) or  # Horizontal
                            self.check_line(row, col, 1, 1) or  # Diagonal /
                            self.check_line(row, col, 1, -1)):  # Diagonal \
                        return True
        return False

    def check_line(self, start_row, start_col, step_row, step_col):
        count = 0
        for _ in range(4):
            if (0 <= start_row < 6 and 0 <= start_col < 7 and
                    self.board[start_row][start_col] == self.current_player):
                count += 1
            else:
                return False
            start_row += step_row
            start_col += step_col
        return count == 4

    def switch_player(self):
        self.current_player = '⚪' if self.current_player == '🔴' else '🔴'

    def get_user_input(self):
        while True:
            user_input = input(f"Player {self.current_player}, choose a column (1-7) or 'U' to undo: ").strip().upper()
            if user_input == 'U':
                self.undo_move()
                return None
            try:
                col = int(user_input) - 1
                if 0 <= col <= 6 and self.is_valid_move(col):
                    return col
                else:
                    print("Invalid move! Please try again.")
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 7.")

    def play_against_ai(self):
        return random.choice([col for col in range(7) if self.is_valid_move(col)])

    def play(self):
        ai_mode = input("Do you want to play against the AI? (yes/no): ").strip().lower() == 'yes'
        while True:
            self.print_board()
            if ai_mode and self.current_player == '⚪':
                print("AI is making a move...")
                time.sleep(1)
                col = self.play_against_ai()
            else:
                col = self.get_user_input()
                if col is None:  # Undo move case
                    continue

            self.make_move(col)
            if self.check_win():
                self.print_board()
                print(f"Player {self.current_player} wins!")
                break
            elif ' ' not in [cell for row in self.board for cell in row]:
                self.print_board()
                print("It's a draw!")
                break
            self.switch_player()

        if input("Do you want to play again? (yes/no): ").strip().lower() == 'yes':
            self.reset_game()
            self.play()
        else:
            print("Thanks for playing!")

    def reset_game(self):
        self.__init__()
        self.switch_starting_player()

    def switch_starting_player(self):
        self.first_turn_player = '⚪' if self.first_turn_player == '🔴' else '🔴'
        self.current_player = self.first_turn_player


def play():
    game = ConnectFour()
    game.play()


if __name__ == "__main__":
    play()
