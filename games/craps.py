import random

from halo import Halo
from loguru import logger
from rich.prompt import Prompt


class Craps:
    def __init__(self):
        self.balance = 1000

    @staticmethod
    def roll_dice():
        return random.randint(1, 6) + random.randint(1, 6)

    def place_bet(self, bet_type, bet_amount):
        if bet_amount > self.balance:
            logger.error("Insufficient balance for bet.")
            return False
        self.balance -= bet_amount
        logger.info(f"[bold green]💰 {bet_type} Bet of ${bet_amount} placed.[/bold green]")
        return True

    def pass_line_bet(self, bet_amount):
        if self.place_bet("Pass Line", bet_amount):
            # Add game logic for Pass Line bet here
            pass

    def dont_pass_line_bet(self, bet_amount):
        if self.place_bet("Don't Pass Line", bet_amount):
            # Add game logic for Don't Pass Line bet here
            pass

    def odds_bet(self, bet_amount):
        if self.place_bet("Odds", bet_amount):
            # Add game logic for Odds bet here
            pass

    def field_bet(self, bet_amount):
        if self.place_bet("Field", bet_amount):
            # Add game logic for Field bet here
            pass

    def come_bet(self, bet_amount):
        if self.place_bet("Come", bet_amount):
            # Add game logic for Come bet here
            pass

    @staticmethod
    def cpu_logic(player_roll):
        # Implement CPU logic here
        # Example: CPU decides to roll again if player rolled higher than 7
        if player_roll > 7:
            logger.info("[bold blue]🎲 CPU decides to roll again.[/bold blue]")
            return True
        else:
            logger.info("[bold blue]🎲 CPU decides to stay.[/bold blue]")
            return False

    def play(self):
        logger.info("[bold yellow]🎲 Welcome to Craps! You start with $1000.[/bold yellow]")
        while self.balance > 0:
            logger.info(f"[bold cyan]💰 Your current balance: ${self.balance}[/bold cyan]")
            choice = Prompt.ask("[bold]Do you want to (r)oll or (q)uit?[/bold]").lower()
            if choice == 'q':
                logger.info(f"[bold magenta]👋 Thanks for playing! You leave with ${self.balance}.[/bold magenta]")
                return
            elif choice == 'r':
                bet_amount_str = Prompt.ask("Enter the bet amount: ")
                bet_amount = int(bet_amount_str)
                self.pass_line_bet(bet_amount)
                self.dont_pass_line_bet(bet_amount)
                self.odds_bet(bet_amount)
                self.field_bet(bet_amount)
                self.come_bet(bet_amount)
                with Halo(text='🎲 Rolling the dice...', spinner='dots'):
                    player_roll = self.roll_dice()
                    logger.info(f"[bold green]🎲 You rolled: {player_roll}[/bold green]")
                    continue_rolling = self.cpu_logic(player_roll)
                    if continue_rolling:
                        cpu_roll = self.roll_dice()
                        logger.info(f"[bold blue]🎲 CPU rolled: {cpu_roll}[/bold blue]")
                    else:
                        cpu_roll = None
                if cpu_roll is not None:
                    if player_roll > cpu_roll:
                        logger.info("[bold green]🎉 You win this round![/bold green]")
                        self.balance += bet_amount  # Increase the balance by the bet amount for a win
                    elif player_roll < cpu_roll:
                        logger.info("[bold red]😢 CPU wins this round![/bold red]")
                        self.balance -= bet_amount  # Decrease the balance by the bet amount for a loss
                    else:
                        logger.info("[bold yellow]😐 It's a tie![/bold yellow]")
                input("Press Enter to continue...")
            else:
                logger.info("[bold red]❌ Invalid choice. Please choose 'r' to roll or 'q' to quit.[/bold red]")
        logger.info(f"[bold cyan]💰 Your final balance: ${self.balance}. Thanks for playing![/bold cyan]")


def play():
    game = Craps()
    game.play()


if __name__ == "__main__":
    play()
