from backend.player import Piece
from utils.invalidMoveException import InvalidMoveException

class Board:
    # Use list as a stack push === append, pop === pop 
    def __init__(self):
        # Initializing all 4x4 cells to None
        self.grid = [[[None] for _ in range(4)] for _ in range(4)]


    def addPiece(self, row: int, column: int, piece: Piece):
        """ Add piece from your external stack to the board """
        
        assert row < 4 and column < 4
        assert isinstance(piece, Piece)
        
        
        if self.grid[row][column][-1] is None:
            self.grid[row][column].append(piece)
        else:
            existingPiece = self.grid[row][column][-1]
            if piece.size > existingPiece.size:
                self.grid[row][column].append(piece)
            else:
                raise InvalidMoveException("Invalid move, you can't add your piece on top of larger piece.")
        
        
    def movePiece(self, oldRow: int, oldColumn: int, newRow: int, newColumn: int):
        """ Move a piece that is already on the board """
        
        piece = self.grid[oldRow][oldColumn][-1]
        assert piece is not None
        
        self.grid[oldRow][oldColumn].pop()
        
        self.addPiece(newRow, newColumn, piece)
        

if __name__ == "__main__":
    board = Board()
    print(board.grid)