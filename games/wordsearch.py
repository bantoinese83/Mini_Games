import random
import time
from random_word import RandomWords
from tqdm import tqdm


class WordSearch:
    def __init__(self, word_list=None, time_limit=60):
        self.word_list = word_list if word_list else []
        self.size = max(len(word) for word in self.word_list)  # Set the size to the length of the longest word
        self.grid = [['' for _ in range(self.size)] for _ in range(self.size)]  # Initialize the grid
        self.found_words = []
        self.time_limit = time_limit
        self.start_time = None

    def generate_grid(self):
        # Fill the grid with random letters
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = chr(random.randint(65, 90))

    def add_word(self, word):
        # Add word to the grid randomly
        if len(word) > self.size:
            print(f"Skipping word {word} as it is longer than the grid size.")
            return

        direction = random.choice(['horizontal', 'vertical', 'diagonal'])
        if direction == 'horizontal':
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - len(word))
            for i in range(len(word)):
                self.grid[row][col + i] = word[i]
        elif direction == 'vertical':
            row = random.randint(0, self.size - len(word))
            col = random.randint(0, self.size - 1)
            for i in range(len(word)):
                self.grid[row + i][col] = word[i]
        else:  # diagonal
            row = random.randint(0, self.size - len(word))
            col = random.randint(0, self.size - len(word))
            while row + len(word) > self.size or col + len(word) > self.size:  # Ensure diagonal within bounds
                row = random.randint(0, self.size - 1)
                col = random.randint(0, self.size - 1)
            for i in range(len(word)):
                self.grid[row + i][col + i] = word[i]

    def display_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] in self.found_words:
                    print('\033[92m' + self.grid[i][j] + '\033[0m', end=' ')  # Green color for found words
                else:
                    print(self.grid[i][j], end=' ')
            print()
        print()

    def find_word(self, word):
        # Search for the word in the grid
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == word[0]:
                    # Check horizontally
                    if ''.join(self.grid[i][j:j + len(word)]) == word:
                        return True, 'horizontal', i, j
                    # Check vertically
                    if ''.join([self.grid[i + k][j] for k in range(len(word)) if i + k < self.size]) == word:
                        return True, 'vertical', i, j
                    # Check diagonally
                    if ''.join([self.grid[i + k][j + k] for k in range(len(word)) if
                                i + k < self.size and j + k < self.size]) == word:
                        return True, 'diagonal', i, j
        return False, None, None, None

    def play(self):
        self.generate_grid()
        for word in self.word_list:
            self.add_word(word)

        self.display_grid()

        print("Find these words:")
        for word in self.word_list:
            print(word)

        print("\nInstructions:")
        print("1. Look for the words in the grid. They can be arranged horizontally, vertically, or diagonally.")
        print("2. Once you find a word, enter it exactly as it appears in the 'Find these words:' list.")
        print("3. You have a time limit to find all the words. The progress bar below shows the remaining time.\n")

        self.start_time = time.time()
        with tqdm(total=self.time_limit, desc="Time remaining") as pbar:
            while len(self.found_words) < len(self.word_list):
                elapsed_time = time.time() - self.start_time
                if elapsed_time > self.time_limit:
                    print("\nTime's up!")
                    break

                pbar.update(elapsed_time - pbar.n)  # Update the progress bar

                guess = input("Enter a word: ").upper()  # Convert the guess to uppercase
                if guess in self.word_list:  # Check if the guess is in the word list
                    found, direction, row, col = self.find_word(guess)
                    if found:
                        if guess not in self.found_words:  # Check if the word hasn't been found before
                            print("You found:", guess)
                            self.found_words.append(guess)  # Add the found word to the found_words list
                            self.word_list.remove(guess)  # Remove the found word from the word list

                            # Remove the found word from the grid
                            if direction == 'horizontal':
                                for i in range(len(guess)):
                                    self.grid[row][col + i] = ' '
                            elif direction == 'vertical':
                                for i in range(len(guess)):
                                    self.grid[row + i][col] = ' '
                            else:  # diagonal
                                for i in range(len(guess)):
                                    self.grid[row + i][col + i] = ' '
                        else:
                            print("You already found that word!")
                    else:
                        print("Word not found.")
                else:
                    print("Word not in the list!")

        print("Congratulations! You found all the words.")
        self.display_grid()


def get_random_words(num_words):
    r = RandomWords()
    return [r.get_random_word() for _ in range(num_words)]


def play():
    word_list = get_random_words(5)  # Get 5 random words
    game = WordSearch(word_list=word_list)
    game.play()


if __name__ == "__main__":
    play()
