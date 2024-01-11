from enum import Enum
from src.utils.piece import Piece


class MoveType(Enum):
    ADD = 1
    MOVE = 2

    def __eq__(self, other):
        if isinstance(other, MoveType):
            return self.value == other.value
        return NotImplemented


class Move:
    def __init__(
        self,
        type: MoveType,
        piece: Piece,
        row: int,
        column: int,
        external_row: int = None,
    ):
        self.type = type
        self.piece = piece
        self.row = row
        self.column = column
        external_row = external_row

    def __repr__(self):
        return f"{self.type} {self.piece} to ({self.row}, {self.column})"
