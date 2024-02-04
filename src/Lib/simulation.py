from src.Lib import util
from src.Lib.util import Team, Player, Game


class MonteCarlo:
    """
    Collect data on each player's points scored in past games.
    Fit a distribution (e.g., Poisson, negative binomial, or zero-inflated Poisson) to the data for each player.
    Use Monte Carlo simulation to simulate the total points scored by the team based on the sum of each player's expected points.
    As you get more data from each player, update the distributions using Bayesian inference.
    Repeat the Monte Carlo simulation with the updated distributions to obtain more accurate predictions.
    """
    def __init__(self, game: Game) -> None:
        self.game = game
        self.home = game.home
        self.away = game.away
        

    def run(self, simulations):
        if not hasattr(self, 'rf'):
            raise Exception(f'No random function has been bound to this simulator!')

    def bind(self, rf):
        """
        Bind a random function to this instance
        """
        self.rf = rf