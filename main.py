import time

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from tqdm import tqdm

from games import blackjack, solitare, hangman, mancala, wordsearch, slots, connect4

# CLI Menu options for the games available.
# The keys are the options the user can select,
# and the values are the functions to call.

GAMES = {
    "1": blackjack.play,
    "2": hangman.play,
    "3": mancala.play,
    "4": wordsearch.play,
    "5": slots.play,
    "6": solitare.play,
    "7": connect4.play,
}

# Game names for displaying in the menu
GAME_NAMES = {
    "1": "Blackjack",
    "2": "Hangman",
    "3": "Mancala",
    "4": "Word Search",
    "5": "Slots",
    "6": "Solitaire",
    "7": "Connect Four",
}


def display_menu():
    options = [(f"{key}. {name}", key) for key, name in GAME_NAMES.items()]
    options.append(("Q. Quit", "Q"))
    return options


def show_progress_bar():
    for _ in tqdm(range(100), desc="Launching game", ncols=100, ascii=True):
        time.sleep(0.02)  # Simulate loading time


def main():
    """
    Main function to run the game menu.
    """
    print("Welcome to the game center!")

    menu_completer = WordCompleter(list(GAMES.keys()) + ["Q"], ignore_case=True)
    menu_history = InMemoryHistory()

    while True:
        options = display_menu()
        print("\n".join(option[0] for option in options))
        choice = prompt("Choose a game to play: ", completer=menu_completer, history=menu_history).upper()

        if choice == "Q":
            print("Thanks for playing!")
            break

        if choice in GAMES:
            show_progress_bar()
            GAMES[choice]()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
