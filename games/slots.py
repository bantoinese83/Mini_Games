import random

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

# Symbol configuration
symbol_count = {"A": 2, "B": 4, "C": 6, "D": 8}
symbol_value = {"A": 5, "B": 4, "C": 3, "D": 2}


def check_winning_lines(columns, lines):
    """
    Check if there are any winning lines in the provided columns.

    Args:
        columns (list): List of columns, each containing symbols for each row.
        lines (int): Number of lines to check for winning.

    Returns:
        list: List of winning line numbers.
    """
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winning_lines.append(line + 1)
    return winning_lines


def calculate_winnings(columns, lines, bet):
    """
    Calculate the total winnings based on the provided columns and bet.

    Args:
        columns (list): List of columns, each containing symbols for each row.
        lines (int): Number of lines bet on.
        bet (int): Bet amount per line.

    Returns:
        int: Total winnings.
    """
    winnings = 0
    winning_lines = check_winning_lines(columns, lines)
    for line in winning_lines:
        symbol = columns[0][line - 1]
        winnings += symbol_value[symbol] * bet
    return winnings


def generate_slot_machine_spin(rows, cols, symbols):
    """
    Generate a random spin result for the slot machine.

    Args:
        rows (int): Number of rows in the slot machine.
        cols (int): Number of columns in the slot machine.
        symbols (dict): Dictionary containing symbols and their counts.

    Returns:
        list: List of columns, each containing symbols for each row.
    """
    all_symbols = [symbol for symbol, count in symbols.items() for _ in range(count)]
    columns = []
    for _ in range(cols):
        column = random.sample(all_symbols, rows)
        columns.append(column)
    return columns


def print_slot_machine(columns):
    """
    Print the current state of the slot machine.

    Args:
        columns (list): List of columns, each containing symbols for each row.
    """
    for row in zip(*columns):
        print(" | ".join(row))


def get_valid_input(prompt, input_type, validation_func):
    """
    Get valid input from the user.

    Args:
        prompt (str): The prompt to display to the user.
        input_type (type): The type of input expected.
        validation_func (function): A function to validate the input.

    Returns:
        input_type: The valid input provided by the user.
    """
    while True:
        user_input = input(prompt)
        try:
            user_input = input_type(user_input)
            if validation_func(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please try again.")


def deposit():
    """
    Prompt the user to deposit an initial amount.

    Returns:
        int: The deposited amount.
    """
    return get_valid_input("What would you like to deposit? $", int, lambda x: x > 0)


def get_number_of_lines():
    """
    Get the number of lines the user wants to bet on.

    Returns:
        int: Number of lines.
    """
    return get_valid_input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ", int, lambda x: 1 <= x <= MAX_LINES)


def get_bet():
    """
    Get the bet amount per line from the user.

    Returns:
        int: Bet amount.
    """
    return get_valid_input(f"What would you like to bet on each line? (${MIN_BET}-{MAX_BET}): ", int,
                           lambda x: MIN_BET <= x <= MAX_BET)


def play_round(balance):
    """
    Perform a single round of the slot machine game.

    Args:
        balance (int): Current balance of the player.

    Returns:
        int: Updated balance after the round.
    """
    lines = get_number_of_lines()
    bet = get_bet()
    total_bet = bet * lines

    if total_bet > balance:
        print(f"You do not have enough to bet that amount, your current balance is: ${balance}")
        return balance

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = generate_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)

    winnings = calculate_winnings(slots, lines, bet)
    print(f"You won ${winnings}.")
    return balance + winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press enter to play (q to quit). ")
        if answer.lower() == "q":
            break
        balance = play_round(balance)
    print(f"You left with ${balance}")


def play():
    main()
