from enum import Enum

class GameModes(Enum):
    HumanVsHuman: int = 0
    HumanVsAi: int = 1
    AiVsAi: int = 2

    def __eq__(self, other):
        if isinstance(other, GameModes):
            return self.value == other.value
        return NotImplemented