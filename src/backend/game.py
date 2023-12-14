from src.backend.board import Board
from src.backend.player import *
from src.utils.gameModesEnum import *

from src.backend.player import Person, Color, Piece
from src.utils.gameModesEnum import GameModes


class Game:
    def __init__(self, mode: GameModes, player1Name: str, player2Name: str, player1Color: Color, player2Color: Color):
        self.board = Board()
        
        if mode == GameModes.HumanVsHuman:
            self.player1 = Person(player1Color, player1Name)
            self.player2 = Person(player2Color, player2Name)
        elif mode == GameModes.HumanVsAi:
            self.player1 = Person(player1Color, player1Name)
            self.player2 = None #TODO: Use the Ai Class when implemented
        elif mode == GameModes.AiVsAi:
            self.player1 = None #TODO: Use the Ai Class when implemented
            self.player2 = None #TODO: Use the Ai Class when implemented
        
        self.turn = self.player1 if player1Color == Color.WHITE else self.player2
        
    def addGobblet(self, row: int, column: int, piece: Piece):
        " Add gobblet from the external stack "
        self.board.addPiece(row, column, piece)
    
    def moveGobblet(self, oldRow: int, oldColumn: int, newRow: int, newColumn: int):
        " Move already existent gobblet to new location "
        self.board.movePiece(oldRow, oldColumn, newRow, newColumn)
    
    def statusCheck(self):
        pass
    
    def drawState(self):
        pass
    
    def winState(self):
        white = self.board.getLinedUpGobblets(Color.WHITE)
        black = self.board.getLinedUpGobblets(Color.BLACK)
        
        white = [gobblet for gobblet in white if len(gobblet) == 4]
        black = [gobblet for gobblet in black if len(gobblet) == 4]
        
        if len(white) > 0:
            return self.player1 if self.player1.color == Color.WHITE else self.player2
        elif len(black) > 0:
            return self.player1 if self.player1.color == Color.BLACK else self.player2
        else:
            return None