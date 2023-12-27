import uuid

from player import *
from uuid import uuid1

class AI(Player):
    def __init__(self, color: Color):
        Player.__init__(self, color)
        self.icon = None
        self.id = "AI: "+uuid.uuid1().__str__()

    def __str__(self):
        return f"AI: Color({self.color})"

    def __del__(self):
        pass


if __name__ == '__main__':
    pass
