import random

from random_word import RandomWords


class HangmanGame:
    def __init__(self, difficulty="medium"):
        self.r = RandomWords()
        self.words = [self.r.get_random_word() for _ in range(100)]
        self.difficulty_levels = {"easy": 10, "medium": 7, "hard": 5}
        self.max_guesses = self.difficulty_levels.get(difficulty, 7)
        self.hangman_stages = [
            '''
               ____
              |    |      
              |    o      
              |       
              |    
              |   
             _|_
            |   |______
            |          |
            |__________|
            ''',
            '''
               ____
              |    |      
              |    o      
              |    |
              |    
              |   
             _|_
            |   |______
            |          |
            |__________|
            ''',
            '''
               ____
              |    |      
              |    o      
              |   /|
              |    
              |   
             _|_
            |   |______
            |          |
            |__________|
            ''',
            '''
               ____
              |    |      
              |    o      
              |   /|\\
              |    
              |   
             _|_
            |   |______
            |          |
            |__________|
            ''',
            '''
               ____
              |    |      
              |    o      
              |   /|\\
              |    |
              |   
             _|_
            |   |______
            |          |
            |__________|
            ''',
            '''
               ____
              |    |      
              |    o      
              |   /|\\
              |    |
              |   / 
             _|_
            |   |______
            |          |
            |__________|
            ''',
            '''
               ____
              |    |      
              |    o      
              |   /|\\
              |    |
              |   / \\
             _|_
            |   |______
            |          |
            |__________|
            '''
        ]
        self.secret_word = None
        self.display_word = None
        self.guesses = 0
        self.hints_used = 0
        self.score = 0
        self.game_over = False
        self.reset_game()

    def process_guess(self, guess):
        if guess in self.secret_word:
            for i, letter in enumerate(self.secret_word):
                if letter == guess:
                    self.display_word[i] = letter
                    self.score += 1
        else:
            self.guesses += 1
            print(self.hangman_stages[self.guesses - 1])  # print the hangman figure
            print(f"You have {self.max_guesses - self.guesses} guesses left")

    def is_game_over(self):
        if self.guesses >= self.max_guesses:
            print("You lose")
            return True
        if "_" not in self.display_word:
            print("You win")
            return True
        return False

    def give_hint(self):
        if self.hints_used < 3:
            unrevealed_letters = [letter for i, letter in enumerate(self.secret_word) if self.display_word[i] == '_']
            if unrevealed_letters:
                hint = random.choice(unrevealed_letters)
                self.hints_used += 1
                self.score -= 1
                print(f"Hint: There is a '{hint}' in the word")
            else:
                print("All letters have been revealed. No hints available.")
        else:
            print("You have used all your hints.")

    def play(self):
        print("Welcome to Hangman!")
        print(f"You get {self.max_guesses} guesses")
        print(' '.join(self.display_word))

        while not self.game_over:
            guess = input("Guess a letter or type 'hint' for a hint: ").lower()
            if guess == 'hint':
                self.give_hint()
            else:
                self.process_guess(guess)
                print(' '.join(self.display_word))
                self.game_over = self.is_game_over()

        print(f"Your score: {self.score}")
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again == 'y':
            self.reset_game()
            self.play()

    def reset_game(self):
        self.secret_word = random.choice(self.words)
        self.display_word = ['_' for _ in self.secret_word]
        self.guesses = 0
        self.hints_used = 0
        self.score = 0
        self.game_over = False


def play():
    game = HangmanGame()
    game.play()
