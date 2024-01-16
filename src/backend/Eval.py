from src.backend.AI import AI
from src.backend.player import Player, Piece
from src.backend.board import Board
from src.backend.Person import Person
from typing import Optional, Tuple
from src.utils.piece import Color


class Evaluation:
    def __init__(self):
        self.board: Optional[Board] = None
        self.min: Optional[Player] = None
        self.max: Optional[Player] = None
        self.num_max_external = 0
        self.num_min_eternal = 0

    def heuristic_v2(self, board: Board, minimizer: Player, maximizer: Player):
        """
                    if direction consists only of SINGLE COLOR:
                        - each empty field Scored 1
                        - For each piece multiple with 10 or any number

                    if there exists MIXED COLORS in the direction:
                     - #Pieces of MIN player < #Pieces of MAX outside the board
                        do the same as above
                     - otherwise 0 rate
        """
        self.min, self.max = minimizer, maximizer
        self.num_max_external, self.num_min_eternal = self.num_external_pieces()
        self.board = board

        score = 0
        score += self.evaluate_cols()
        score += self.evaluate_rows()
        score += self.evaluate_diagonals()

        return score

    def evaluate_rows(self) -> int:
        assert self.min is not None and self.max is not None
        score = 0
        for row in self.board.grid:
            score += self.get_pieces_score(row)
        return score

    def evaluate_cols(self) -> int:
        pass

    def evaluate_diagonals(self) -> int:
        pass

    def get_pieces_score(self, pieces: list[Piece]):
        unique = Evaluation.check_uniqueness(pieces)
        if not unique:
            pass
        else:
            pass

    def num_external_pieces(self) -> Tuple[int, int]:
        num_min, num_max = 0, 0
        for i in range(3):
            num_min += len(self.min.pieces[i]) if self.min.pieces[i] else 0
            num_max += len(self.max.pieces[i]) if self.max.pieces[i] else 0
        return num_min, num_max
    @classmethod
    def check_uniqueness(cls, pieces: list[Piece]) -> bool:
        color = None
        for piece in pieces:
            if piece is None:
                continue
            else:
                if color is None:
                    color = piece.color
                elif color != piece.color:
                    return False
        return True


if __name__ == '__main__':
    eval = Evaluation()
    board = Board()
    ai = AI(color=Color.WHITE)
    person = Person(color=Color.BLACK)
    eval.heuristic_v2(board=board,
                      minimizer=ai,
                      maximizer=person)
