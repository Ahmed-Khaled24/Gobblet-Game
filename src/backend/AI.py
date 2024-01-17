import uuid

from src.backend.player import *
from uuid import uuid1


class AI(Player):
    def __init__(self, color: Color, name, difficulty: int = 2):
        Player.__init__(self, color)
        self.name = name
        self.icon = None
        self.id = "AI: " + uuid.uuid1().__str__()
        self.difficulty = difficulty

    def __str__(self):
        return f"AI: Color({self.color})"

    def __del__(self):
        pass


if __name__ == "__main__":
    pass
