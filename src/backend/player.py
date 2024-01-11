from src.utils.piece import Color, Piece, PieceSize


class Player:
    """The abstract class for the player. It contains the basic information about the player and the pieces that he has"""

    def __init__(self, color: Color):
        self.color: Color = color
        self.pieces: list[list] = []
        self.initial_state = None
        self.all_pieces: list[PieceSize] = [
            PieceSize.VERYSMALL,
            PieceSize.SMALL,
            PieceSize.MEDIUM,
            PieceSize.LARGE,
        ]  # used for initialization
        self.__initialize_pieces()

    def __initialize_pieces(self) -> None:
        for i in range(3):
            full_stack_pieces = []
            for size in self.all_pieces:
                full_stack_pieces.append(Piece(self.color, size, i))
            self.pieces.append(full_stack_pieces)

    def remove_from_external_stack(self, raw_number: int) -> Piece | None:
        if raw_number not in range(3):
            return None
        return self.pieces[raw_number].pop()

    def __del__(self):
        pass

    def __str__(self):
        pass

    def print_pieces(self):
        for i in range(len(self.pieces)):
            for j in range(len(self.pieces[i])):
                print(self.pieces[i][j], end=" ")
            print("\n")

    def getSize(piece):
        return piece.value
