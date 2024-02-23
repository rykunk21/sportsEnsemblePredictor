from typing import Any



class Node:
    adj = {}
    def __init__(self, value: Any = None) -> None:
        self.value = value

class Prob(float):
    def __init__(self, value):
        if value > 1 or value < 0:
            raise Exception(f'Value {value} is invalid probability')
        self.value = value

    def __bool__(self):
        return self.value > 0.5

    def __float__(self):
        return self.value

    def __invert__(self):
        return Prob(1 - self.value)