from src.backend.board import Board
from src.backend.player import *
from src.utils.gameModesEnum import *
from enum import Enum
from src.backend.player import Person, Color, Piece
from src.utils.gameModesEnum import GameModes
from src.utils.drawException import DrawException
from src.backend.ai_player import AI


class GameStatus(Enum):
    Win = 1
    Draw = 2
    OnGame = 3

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class Game:
    def __init__(self, mode: GameModes, player1Name: str, player2Name: str, player1Color: Color, player2Color: Color):
        self.board = Board()
        self.turn = Color.WHITE
        if mode == GameModes.HumanVsHuman:
            self.player1: Player = Person(player1Color, player1Name)
            self.player2 = Person(player2Color, player2Name)
        elif mode == GameModes.HumanVsAi:
            self.player1 = Person(player1Color, player1Name)
            self.player2 = AI(player2Color)
        elif mode == GameModes.AiVsAi:
            self.player1 = AI(player1Color)
            self.player2 = AI(player2Color)
        self.game_status: GameStatus = GameStatus.OnGame
        self.winner = None

    def changeTurn(self):
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE

    def addGobblet(self, row: int, column: int, piece: Piece):
        " Add gobblet from the external stack "
        try:
            if piece.color == self.player1.color:
                self.board.addPiece(row, column, piece, self.player1)
            else:
                self.board.addPiece(row, column, piece, self.player2)
            self.changeTurn()
        except DrawException as err:
            self.game_status = GameStatus.Draw

    def moveGobblet(self, oldRow: int, oldColumn: int, newRow: int, newColumn: int):
        " Move already existent gobblet to new location "
        self.board.movePiece(oldRow, oldColumn, newRow, newColumn)
        self.changeTurn()

    def statusCheck(self) -> Tuple[Optional[Player], GameStatus]:
        if self.game_status == GameStatus.Win:
            return self.winner, self.game_status
        else:
            return None, self.game_status

    def winState(self):
        white = self.board.getLinedUpGobblets(Color.WHITE)
        black = self.board.getLinedUpGobblets(Color.BLACK)

        white = [gobblet for gobblet in white if len(gobblet) == 4]
        black = [gobblet for gobblet in black if len(gobblet) == 4]

        if len(white) > 0:
            self.winner = self.player1 if self.player1.color == Color.WHITE else self.player2
            self.game_status = GameStatus.Win
        elif len(black) > 0:
            self.winner = self.player1 if self.player1.color == Color.BLACK else self.player2
            self.game_status = GameStatus.Win


