from src.Lib import util
from src.Lib.util import Team, Player, Game
from src.Lib.data import simHandler

import numpy as np
from scipy.stats import norm

class MonteCarlo:
    """
    Collect data on each player's points scored in past games.
    Fit a distribution (e.g., Poisson, negative binomial, or zero-inflated Poisson) to the data for each player.
    Use Monte Carlo simulation to simulate the total points scored by the team based on the sum of each player's expected points.
    As you get more data from each player, update the distributions using Bayesian inference.
    Repeat the Monte Carlo simulation with the updated distributions to obtain more accurate predictions.
    """
    def __init__(self, home: str, away: str) -> None:

        home = simHandler.getTeam(home)
        away = simHandler.getTeam(away)

        self.game = Game.NCAAB(home, away)
        self.homeRoster = self.game.homeRoster
        self.awayRoster = self.game.awayRoser
        

    def run(self, simulations):
        
        
        homePoints = []
        for player in self.homeRoster:
            points = self.game.getPlayerPoints(player)
            
            mean = np.mean(points)
            std = np.std(points)

            dist = np.random.normal(mean, std, simulations)
            homePoints.append(dist)

        awayPoints = []
        for player in self.awayRoster:

            points = self.game.getPlayerPoints(player)
            
            mean = np.mean(points)
            std = np.std(points)

            dist = np.random.normal(mean, std, simulations)
            awayPoints.append(dist)


        homePoints = np.array(homePoints)
        homePoints[np.isnan(homePoints)] = 0
        homePoints[homePoints < 0 ] = 0


        awayPoints = np.array(awayPoints)
        awayPoints[np.isnan(awayPoints)] = 0
        awayPoints[awayPoints < 0] = 0

        homeWinProb = 0
        spreads = []
        for i in range(simulations):
            homeScore = sum(homePoints[:,i])
            awayScore = sum(awayPoints[:,i])
        
            homeWinProb += 1 if homeScore >= awayScore else 0

            spreads.append(awayScore - homeScore)

        homeWinProb /= simulations
        
        return homeWinProb, np.array(spreads)
    

    def probability_of_value(self, values, value):
        mean = np.mean(values)
        std = np.std(values)
        distribution = norm(loc=mean, scale=std)
        probability = distribution.cdf(value)
        return probability