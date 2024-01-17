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

    def heuristic_v2(self, board: Board, minimizer: Player, maximizer: Player):
        """
        if direction consists only of SINGLE COLOR:
            - each empty field Scored 1
            - For each piece multiple with 10 or any number

        if there exists MIXED COLORS in the direction:
         - size of Pieces of MIN player < #Pieces of MAX outside the board
            do the same as above
         - otherwise 0 rate
        """
        self.min, self.max = minimizer, maximizer
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
            score += self.get_pieces_score([element[-1] for element in row])
        return score

    def evaluate_cols(self) -> int:
        assert self.min is not None and self.max is not None
        score = 0
        for i in range(4):
            score += self.get_pieces_score([row[i][-1] for row in self.board.grid])
        return score

    def evaluate_diagonals(self) -> int:
        main_diagonal = []
        anti_diagonal = []
        for i in range(4):
            for j in range(4):
                if i == j:
                    main_diagonal.append(self.board.grid[i][j][-1])
                if i + j + 1 == 4:
                    anti_diagonal.append(self.board.grid[i][j][-1])
        score = self.get_pieces_score(main_diagonal)
        score += self.get_pieces_score(anti_diagonal)
        return score

    def get_pieces_score(self, pieces: list[Piece]) -> int:
        unique = Evaluation.check_uniqueness(pieces)
        score = 1
        color = None
        if not unique:
            # case: number of whites equal number of blacks
            # state will be equal to zero

            num_white, num_black = Evaluation.count_pieces_in_direction(pieces)
            color_dominate = Color.BLACK if num_white < num_black else Color.WHITE
            if num_black == num_white:
                return 0

            pieces_for_another_color = [
                piece for piece in pieces if piece and piece.color != color_dominate
            ]
            player_dominate = self.max if self.max.color == color_dominate else self.min
            has_large_piece = False
            piece_to_compare = pieces_for_another_color[0]
            for st in player_dominate.pieces:
                if st and st[-1].size > piece_to_compare.size:
                    has_large_piece = True
                    break
            if not has_large_piece:
                return 0

            for piece in pieces:
                if piece and piece.color == color_dominate:
                    score *= piece.size.value * 10
            return score if color_dominate == self.max.color else score * -1
        else:
            for piece in pieces:
                if piece:
                    if color is None:
                        color = piece.color
                    score *= piece.size.value * 10
            if not color:
                return 0
            return score if color == self.max.color else score * -1

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

    @classmethod
    def count_pieces_in_direction(cls, pieces: list[Piece]) -> Tuple[int, int]:
        count_w, count_b = 0, 0
        for piece in pieces:
            if not piece:
                continue
            if piece.color == Color.WHITE:
                count_w += 1
            elif piece.color == Color.BLACK:
                count_b += 1
        return count_w, count_b


if __name__ == "__main__":
    pass
    # eval = Evaluation()
    # board = Board()
    # ai = AI(color=Color.WHITE)
    # person = Person(color=Color.BLACK)
    # print(eval.heuristic_v2(board=board,
    #                   minimizer=ai,
    #                   maximizer=person))
