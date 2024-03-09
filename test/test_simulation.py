from src.Lib import simulation, data, util
from src.Lib.util import convertline

import numpy as np
import matplotlib.pyplot as plt

import time
import random

import pickle


def test_simulation():
    # Test with positive numbers
    assert True


def test_monteCarlo():
    """
    Define distributions for each random variable, and sample from an equation
    """
    
    SPREAD = -5
    HOMEMLPROB = -245
    HOMESPREADPROB = -115

    AWAYMLPROB = +200
    AWAYSPREADPROB = -105

    HOME = 'marquette'
    AWAY = 'connecticut'

    home_team = HOME
    away_team = AWAY

    sim = simulation.MonteCarlo(HOME, AWAY)
    prob, spreads = sim.run(10000)
    
    spreadProb = sim.probability_of_value(spreads, SPREAD)

    home_ml_odds, away_ml_odds = HOMEMLPROB, AWAYMLPROB
    home_spread_odds, away_spread_odds = HOMESPREADPROB, AWAYSPREADPROB

    fieldWidth = max(
                len(home_team + ' cover:'), 
                len(home_team + ' ML:'), 
                len(away_team + ' cover'), 
                len(away_team + ' ML:'),
                len(f'Spread {np.mean(spreads):.2f}')
            )
        

    print('-' * (fieldWidth + 30))
    print('{:^{width}}|{:^15}|{:^15}'.format(f'Spread {np.mean(spreads):.2f}', 'Prob', 'Diff', width=fieldWidth))
    print('-' * (fieldWidth + 30))  # Adjust the total width as needed

    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{home_team} cover:', spreadProb, 
        spreadProb - convertline(home_spread_odds), width=fieldWidth)
    )
    
    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{home_team} ML:', prob, 
        prob - convertline(home_ml_odds), width=fieldWidth)
    )
    
    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{away_team} cover', 1 - spreadProb, 
        (1 - spreadProb) - convertline(away_spread_odds), width=fieldWidth)
    )
    
    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{away_team} ML:', 1 - prob, 
        (1 - prob) - convertline(away_ml_odds), width=fieldWidth)
    )



