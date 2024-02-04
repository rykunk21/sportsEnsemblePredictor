
class RandomVariable:
    pass


class RandomFunction:
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
            self.home = home
            self.away = away

        def __str__(self) -> str:
            return f'Game(home: {self.home} vs away: {self.away})'
        
        def __repr__(self) -> str:
            return self.__str__()
        

        def randomFunction(self):
            """
            return the rf associated with the game
            """
            return RandomFunction()