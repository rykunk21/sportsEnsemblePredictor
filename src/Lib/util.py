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
                return [int(row[-1]) if not np.isnan(int(row[-1])) else 0 for row in player.rows][:-1]
    
            elif name in self.awayRoser.keys():
                player = self.awayRoser.get(name)
                return [int(row[-1]) if not np.isnan(int(row[-1])) else 0 for row in player.rows][:-1]
            
            else:
                raise Exception(f'Player {name} not playing in this game!!!')
            

def convertline(line):
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





