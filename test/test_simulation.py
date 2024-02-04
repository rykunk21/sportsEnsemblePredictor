from src.Lib import simulation, data, util

import numpy as np
import matplotlib.pyplot as plt


def test_simulation():
    # Test with positive numbers
    assert True


def test_monteCarlo():
    """
    Define distributions for each random variable, and sample from an equation
    """

    home = data.simHandler.getTeam('michigan-state')
    away = data.simHandler.getTeam('maryland')

    game = util.Game.NCAAB(home, away)

    rf = game.randomFunction()

    sim = simulation.MonteCarlo(game)

    sim.bind(rf)
    sim.run(10000)

    

def test_simHandler():

    db = 'test/resources/testSimDB'
    handler = data.simHandler(db)
    assert not handler.db is None

