import numpy as np
import src

class Distribution:

    def __init__(self) -> None:
        pass

    def sample(self, numSamples):

        return [x for x in range(numSamples)]

class RandomVariable:
    def __init__(self, distribution: Distribution) -> None:
        self.distribution = distribution

    def sample(self):
        pass


class RandomFunction:
    def __init__(self) -> None:
        pass


class Team:
    pass


class Player:
    pass


class Game:
    def __init__(self) -> None:
        pass

    class NCAAB:
        def __init__(self, home, away) -> None:

            self.home = list(home.keys())[0]
            self.away = list(away.keys())[0]
            
            self.homeRoster: dict = home[self.home]
            self.awayRoser: dict = away[self.away]

        def __str__(self) -> str:
            return f'Game(home: {self.home} vs away: {self.away})'
        
        def __repr__(self) -> str:
            return self.__str__()

    

        def getPlayerPoints(self, name):

            if name in self.homeRoster.keys():
                player = self.homeRoster.get(name)
                # DROP TOTALS
                pattern = lambda x: 'Games' in x[0]
                player.drop(pattern)

                return [int(row[-1]) if not np.isnan(int(row[-1])) else 0 for row in player.rows][:-1]
    
            elif name in self.awayRoser.keys():
                player = self.awayRoser.get(name)
                pattern = lambda x: 'Games' in x[0]
                player.drop(pattern)
                return [int(row[-1]) if not np.isnan(int(row[-1])) else 0 for row in player.rows][:-1]
            
            else:
                raise Exception(f'Player {name} not playing in this game!!!')
            

def convertLine(line):
    if line < 0:
        line *= -1
        return line/ (100 + line)
    else:
        return (100/ (100 + line))
    
def invertLine(prob):
    if prob > .5:
        return f'-{100 * prob / (1- prob)}'
    else:
        return f'+{(100 / prob) - 100}'



def printGameResult(game, simProbs):

    """
    simProbs

    0: mean spread
    1: home spread prob
    2: home ml prob
    """

    home = game[0]
    away = game[1]
    home_team = home.name
    away_team = away.name

    home_ml_odds = home.mlOdds
    home_spread_odds = home.spreadOdds

    away_ml_odds = away.mlOdds
    away_spread_odds = away.spreadOdds



    fieldWidth = max(
        len(home_team + ' cover:'), 
        len(home_team + ' ML:'), 
        len(away_team + ' cover'), 
        len(away_team + ' ML:'),
        len(f'Spread {simProbs[0]:.2f}')
    )


    print('-' * (fieldWidth + 30))
    print('{:^{width}}|{:^15}|{:^15}'.format(f'Spread {simProbs[0]:.2f}', 'Prob', 'Diff', width=fieldWidth))
    print('-' * (fieldWidth + 30))  # Adjust the total width as needed

    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{home_team} cover:', simProbs[1], 
        simProbs[1] - convertLine(home_spread_odds), width=fieldWidth)
    )

    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{home_team} ML:', simProbs[2], 
        simProbs[2] - convertLine(home_ml_odds), width=fieldWidth)
    )

    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{away_team} cover', 1 - simProbs[1], 
        (1 - simProbs[1]) - convertLine(away_spread_odds), width=fieldWidth)
    )

    print('{:<{width}}|{:^15.2f}|{:^15.2f}'.format(
        f'{away_team} ML:', 1 - simProbs[2], 
        (1 - simProbs[2]) - convertLine(away_ml_odds), width=fieldWidth)
    )





class SimResult:

    def __init__(self) -> None:
        pass



