import random


class WordSearch:
    def __init__(self, size=10, word_list=None):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.word_list = word_list if word_list else []
        self.found_words = []

    def generate_grid(self):
        # Fill the grid with random letters
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = chr(random.randint(65, 90))

    def add_word(self, word):
        # Add word to the grid randomly
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
            for i in range(len(word)):
                self.grid[row + i][col + i] = word[i]

    def display_grid(self):
        for row in self.grid:
            print(' '.join(row))
        print()

    def find_word(self, word):
        # Search for the word in the grid
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == word[0]:
                    # Check horizontally
                    if ''.join(self.grid[i][j:j + len(word)]) == word:
                        return True
                    # Check vertically
                    if ''.join([self.grid[i + k][j] for k in range(len(word))]) == word:
                        return True
                    # Check diagonally
                    if ''.join([self.grid[i + k][j + k] for k in range(len(word))]) == word:
                        return True
        return False

    def play(self):
        self.generate_grid()
        for word in self.word_list:
            self.add_word(word)

        self.display_grid()

        print("Find these words:")
        for word in self.word_list:
            print(word)

        while len(self.found_words) < len(self.word_list):
            guess = input("Enter a word: ").upper()
            if guess in self.found_words:
                print("You already found that word!")
                continue
            if guess in self.word_list:
                print("You found:", guess)
                self.found_words.append(guess)
            else:
                print("Word not found.")

        print("Congratulations! You found all the words.")


def play():
    word_list = ['PYTHON', 'JAVA', 'C', 'ALGORITHM', 'COMPUTER']
    game = WordSearch(size=10, word_list=word_list)
    game.play()
