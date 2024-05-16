import random

# Constants
MAX_BET = 100
MIN_BET = 1

# Card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Statistics
stats = {'games_played': 0, 'wins': 0, 'losses': 0}

# History
game_history = []


def deal_card():
    """
    Deal a random card from the deck.

    Returns:
        str: The card dealt.
    """
    return random.choice(list(card_values.keys()))


def calculate_hand_value(hand):
    """
    Calculate the value of a hand.

    Args:
        hand (list): List of cards in the hand.

    Returns:
        int: Value of the hand.
    """
    value = sum(card_values[card] for card in hand)
    num_aces = hand.count('A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value


def print_hand(hand, hide_first_card=False):
    """
    Print the current hand.

    Args:
        hand (list): List of cards in the hand.
        hide_first_card (bool): Whether to hide the first card or not.
    """
    if hide_first_card:
        print(f'Hand: {"??":<3} {" ".join(hand[1:])}')
    else:
        print(f'Hand: {" ".join(hand)}')


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


def get_bet(balance):
    """
    Get the bet amount from the player.

    Args:
        balance (int): The current balance of the player.

    Returns:
        int: The bet amount.
    """
    max_bet = min(MAX_BET, balance)
    return get_valid_input(f"How much would you like to bet? ($1-{max_bet}): ", int, lambda x: MIN_BET <= x <= max_bet)


def blackjack():
    """
    Play a game of Blackjack.
    """
    global stats
    global game_history

    balance = 1000
    while True:
        print(f'Your current balance: ${balance}')
        bet = get_bet(balance)

        # Deal initial cards
        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]

        # Player's turn
        print_hand(player_hand)
        while True:
            action = input("Do you want to hit, stand, double down, or split? (h/s/d/p): ").lower()
            if action == 'h':
                player_hand.append(deal_card())
                print_hand(player_hand)
                if calculate_hand_value(player_hand) > 21:
                    print("Busted! You lose.")
                    balance -= bet
                    stats['games_played'] += 1
                    stats['losses'] += 1
                    game_history.append({'bet': bet, 'outcome': 'loss', 'balance': balance})
                    break
            elif action == 's':
                break
            elif action == 'd':
                if balance >= bet * 2:
                    bet *= 2
                    player_hand.append(deal_card())
                    print_hand(player_hand)
                    if calculate_hand_value(player_hand) > 21:
                        print("Busted! You lose.")
                        balance -= bet
                        stats['games_played'] += 1
                        stats['losses'] += 1
                        game_history.append({'bet': bet, 'outcome': 'loss', 'balance': balance})
                        break
                    else:
                        break
                else:
                    print("Not enough balance to double down. Please choose another action.")
            elif action == 'p':
                if player_hand[0] == player_hand[1]:
                    # Split the hand
                    pass  # Implement splitting logic here

        # Dealer's turn
        print("Dealer's hand:")
        print_hand(dealer_hand, hide_first_card=True)
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(deal_card())
            print_hand(dealer_hand, hide_first_card=True)

        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        # Determine winner
        if player_value <= 21 and (player_value > dealer_value or dealer_value > 21):
            print("You win!")
            balance += bet
            stats['games_played'] += 1
            stats['wins'] += 1
            game_history.append({'bet': bet, 'outcome': 'win', 'balance': balance})
        elif player_value == dealer_value:
            print("It's a tie!")
            stats['games_played'] += 1
            game_history.append({'bet': bet, 'outcome': 'tie', 'balance': balance})
        else:
            print("Dealer wins!")
            balance -= bet
            stats['games_played'] += 1
            stats['losses'] += 1
            game_history.append({'bet': bet, 'outcome': 'loss', 'balance': balance})

        print(f'Your balance: ${balance}')
        if balance < MIN_BET:
            print("You don't have enough balance to continue.")
            break

        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

    print("Thanks for playing Blackjack!")


def play():
    """
    Start a game of Blackjack.
    """
    print("Welcome to Blackjack!")
    blackjack()
    print("Game Statistics:")
    print(f"Games played: {stats['games_played']}")
    print(f"Wins: {stats['wins']}")
    print(f"Losses: {stats['losses']}")
    print("Game History:")
    for game in game_history:
        print(f"Bet: ${game['bet']}, Outcome: {game['outcome']}, Balance: ${game['balance']}")
