from enum import Enum


class PieceSize(Enum):
    VERYSMALL: int = 0
    SMALL: int = 1
    MEDIUM: int = 2
    LARGE: int = 3


class Color(Enum):
    WHITE: int = 0
    BLACK: int = 1


class Piece(object):
    def __init__(self, color: Color, size: PieceSize):
        self.color = color
        self.size = size

    def __del__(self):
        pass

    def __str__(self):
        return f"Piece :Color({self.color.name}) size({self.size.name})"


class Player:
    def __init__(self, color: Color):

        self.color: Color = color
        self.pieces: list[list] = []
        self.initial_state = None
        self.all_pieces: list[PieceSize] = [PieceSize.VERYSMALL, PieceSize.SMALL, PieceSize.MEDIUM,
                                            PieceSize.LARGE]  # used for initialization
        self.__initialize_pieces()

    def __initialize_pieces(self) -> None:
        for i in range(3):
            full_stack_pieces = []
            for size in self.all_pieces:
                full_stack_pieces.append(Piece(self.color, size))
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
                print(self.pieces[i][j], end=' ')
            print('\n')


class Person(Player):
    def __init__(self, color: Color, name: str):
        super().__init__(color)
        self.name = name
        self.icon = None

    def __str__(self):
        return f"Person: name({self.name}) color({self.color})"


if __name__ == '__main__':
    p = Person(color=Color.WHITE, name='ahmed')

    p.remove_from_external_stack(1)
    p.print_pieces()
    p.remove_from_external_stack(1)
    p.remove_from_external_stack(1)
    # p.remove_from_external_stack(1)
    p.print_pieces()
