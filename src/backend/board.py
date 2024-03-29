from src.backend.player import Player
from src.utils.invalidMoveException import (
    InvalidMoveException,
    InvalidMovementSamePositionException,
)
from src.utils.piece import Color, Piece


class Board:
    # Use list as a stack push === append, pop === pop
    def __init__(self):
        # Initializing all 4x4 cells to None
        self.grid = [[[None] for _ in range(4)] for _ in range(4)]

    def to_tuple(self):
        # Convert the board to a tuple of tuples
        return tuple(tuple(tuple(cell) for cell in row) for row in self.grid)

    def __hash__(self):
        # Convert the grid to a tuple of tuples and hash it
        return hash(tuple(tuple(tuple(cell) for cell in row) for row in self.grid))

    def __str__(self):
        string = ""
        for row in self.grid:
            string += f"{ [cell for cell in row]}\n"
        return string

    def addPiece(
        self,
        row: int,
        column: int,
        piece: Piece,
        player: Player,
        external_row: int,
        isVirtualMove: bool = False,
    ):
        """Add piece from your external stack to the board"""

        assert row < 4 and column < 4
        assert isinstance(piece, Piece)
        assert 0 <= external_row < 3

        # 1 [4 Pieces]
        # 2 [4 Pieces]
        # 3 [4 Pieces]

        if self.grid[row][column][-1] is None:
            self.grid[row][column].append(piece)
            if not isVirtualMove:
                player.remove_from_external_stack(raw_number=external_row)
                piece.update_pos((row, column))
        else:
            linedUpGobblets = self.getLinedUpGobblets(
                Color.WHITE if piece.color == Color.BLACK else Color.BLACK
            )
            if (
                len(linedUpGobblets) > 0
                and len(
                    [gobblet for gobblet in linedUpGobblets if (row, column) in gobblet]
                )
                > 0
            ):
                existingPiece = self.grid[row][column][-1]
                if piece.size > existingPiece.size:
                    self.grid[row][column].append(piece)
                    if not isVirtualMove:
                        player.remove_from_external_stack(raw_number=external_row)
                        piece.update_pos((row, column))
                else:
                    raise InvalidMoveException(
                        "Invalid move, you can't add your piece on top of larger piece."
                    )
            else:
                raise InvalidMoveException(
                    "Invalid move, you can't add your piece on top of another piece, unless there are 3 lined up."
                )

    def getLinedUpGobblets(self, color: Color) -> list[list[tuple[int, int]]]:
        """Returns a list of list of tuples containing the coordinates of the lined up gobblets"""
        linedUpGobbles = []

        # Count the total number of gobblets of the given color, if less than 3, then we don't care yet.
        count = 0
        for row in range(4):
            for column in range(4):
                if (
                    self.grid[row][column][-1] is not None
                    and self.grid[row][column][-1].color == color
                ):
                    count += 1

        if count < 3:
            return linedUpGobbles

        # Scan rows
        for row in range(4):
            temp = []
            for column in range(4):
                if (
                    self.grid[row][column][-1] is not None
                    and self.grid[row][column][-1].color == color
                ):
                    temp.append((row, column))

            if len(temp) == 4:
                linedUpGobbles.append(temp)
            elif len(temp) == 3:
                # Check if the 3 lined up are adjacent
                if temp[0][1] + 1 == temp[1][1] and temp[1][1] + 1 == temp[2][1]:
                    linedUpGobbles.append(temp)

        # Scan columns
        for column in range(4):
            temp = []
            for row in range(4):
                if (
                    self.grid[row][column][-1] is not None
                    and self.grid[row][column][-1].color == color
                ):
                    temp.append((row, column))

            if len(temp) == 4:
                linedUpGobbles.append(temp)
            elif len(temp) == 3:
                # Check if the 3 lined up are adjacent
                if temp[0][0] + 1 == temp[1][0] and temp[1][0] + 1 == temp[2][0]:
                    linedUpGobbles.append(temp)

        # Scan diagonals
        def scanDiagonal(
            startRow: int,
            startColumn: int,
            rowLimit: int,
            columnLimit: int,
            acceptedLength: int,
            leftDiagonal: bool,
        ):
            temp = []
            row = startRow
            column = startColumn
            while (
                (row >= rowLimit) or (leftDiagonal and row <= rowLimit)
            ) and column <= columnLimit:
                if (
                    self.grid[row][column][-1] is not None
                    and self.grid[row][column][-1].color == color
                ):
                    temp.append((row, column))
                row = row + 1 if leftDiagonal else row - 1
                column += 1

            if len(temp) == acceptedLength:
                linedUpGobbles.append(temp)

        # Right diagonals
        scanDiagonal(
            startRow=2,
            startColumn=0,
            rowLimit=0,
            columnLimit=2,
            acceptedLength=3,
            leftDiagonal=False,
        )
        scanDiagonal(
            startRow=3,
            startColumn=0,
            rowLimit=0,
            columnLimit=3,
            acceptedLength=4,
            leftDiagonal=False,
        )
        scanDiagonal(
            startRow=3,
            startColumn=1,
            rowLimit=1,
            columnLimit=3,
            acceptedLength=3,
            leftDiagonal=False,
        )

        # Left diagonals
        scanDiagonal(
            startRow=1,
            startColumn=0,
            rowLimit=3,
            columnLimit=2,
            acceptedLength=3,
            leftDiagonal=True,
        )
        scanDiagonal(
            startRow=0,
            startColumn=0,
            rowLimit=3,
            columnLimit=3,
            acceptedLength=4,
            leftDiagonal=True,
        )
        scanDiagonal(
            startRow=0,
            startColumn=1,
            rowLimit=2,
            columnLimit=3,
            acceptedLength=3,
            leftDiagonal=True,
        )

        return linedUpGobbles

    def movePiece(
        self,
        oldRow: int,
        oldColumn: int,
        newRow: int,
        newColumn: int,
        isVirtualMove: bool = False,
    ):
        """Move a piece that is already on the board"""
        if (oldRow, oldColumn) == (newRow, newColumn):
            raise InvalidMovementSamePositionException(
                "Invalid move, Due to same position!"
            )

        piece: Piece = self.grid[oldRow][oldColumn][-1]
        assert piece is not None

        self.grid[oldRow][oldColumn].pop()

        if self.grid[newRow][newColumn][-1] is None:
            self.grid[newRow][newColumn].append(piece)
            if not isVirtualMove:
                piece.update_pos((newRow, newColumn))
        else:
            existingPiece = self.grid[newRow][newColumn][-1]
            if piece.size > existingPiece.size:
                self.grid[newRow][newColumn].append(piece)
                if not isVirtualMove:
                    piece.update_pos((newRow, newColumn))
            else:
                raise InvalidMoveException(
                    "Invalid move, you can't add your piece on top of larger piece."
                )


if __name__ == "__main__":
    board = Board()
    print(board.grid)
