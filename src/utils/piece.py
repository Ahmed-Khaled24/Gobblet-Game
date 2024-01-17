from enum import Enum
from typing import Optional, Tuple
from src.utils.drawException import DrawException


class PieceSize(Enum):
    VERYSMALL: int = 1
    SMALL: int = 2
    MEDIUM: int = 3
    LARGE: int = 4

    def __str__(self):
        return self.name

    def __lt__(self, other):
        if isinstance(other, PieceSize):
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, PieceSize):
            return self.value > other.value
        return NotImplemented


class Color(Enum):
    WHITE: str = "R"
    BLACK: str = "B"

    def __str__(self):
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, Color):
            return self.value == other.value
        return NotImplemented


class Piece(object):
    def __init__(self, color: Color, size: PieceSize, externalStackIndex: int = -111):
        self.id = f"{color.__str__()}-{size.__str__()}-{externalStackIndex}"
        self.externalStackIndex = externalStackIndex
        self.color = color
        self.size = size
        self.counter_for_draw = 0
        self.prev_pos: Optional[Tuple[int, int]] = None
        self.cur_pos: Optional[Tuple[int, int]] = None

    def __repr__(self):
        return self.id

    def __update_safely(self, new_pos: Tuple[int, int]):
        self.prev_pos = self.cur_pos
        self.cur_pos = new_pos

    def update_pos(self, new_pos: Tuple[int, int]):
        """
        updating the position of the gobblet safely by tracking the draw situation that will be caused if 3 repetition of the same piece has occurred
        :param new_pos tuple of x and y that will move the Gobblet to it
        """
        if not self.cur_pos:
            self.cur_pos = new_pos
        else:
            if not self.prev_pos:
                self.__update_safely(new_pos)
            else:
                if self.prev_pos == new_pos and (self.counter_for_draw + 1) % 6 != 0:
                    self.counter_for_draw += 1
                    self.__update_safely(new_pos)
                elif self.prev_pos != new_pos:
                    self.counter_for_draw = 0
                    self.__update_safely(new_pos)
                else:
                    raise DrawException("Draw Situation!")
