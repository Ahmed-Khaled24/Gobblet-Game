from src.backend.player import Player
from src.utils.piece import Color


class Person(Player):
    def __init__(self, color: Color, name: str = None):
        super().__init__(color)
        self.name = name
        self.icon = None

    def __str__(self):
        return f"Person: name({self.name}) color({self.color})"


if __name__ == "__main__":
    pass
