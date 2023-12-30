from src.backend.board import Board
from src.backend.player import *
from src.utils.gameModesEnum import *
from enum import Enum
from src.backend.player import Person, Color, Piece
from src.utils.gameModesEnum import GameModes
from src.utils.drawException import DrawException
from src.backend.ai_player import AI
from src.utils.invalidMoveException import InvalidMoveException,InvalidMovementSamePositionException


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
        assert player1Color != player2Color

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

    def __changeTurn(self):
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE

    # 0 <= row <4
    # 0 <= Col <4
    # 0 <= external_row < 3
    def addGobblet(self, row: int, column: int, piece: Piece, external_row: int):
        " Add gobblet from the external stack "
        try:
            if piece.color == self.player1.color:
                self.board.addPiece(row, column, piece, self.player1, external_row)
            else:
                self.board.addPiece(row, column, piece, self.player2, external_row)
            self.__changeTurn()
        except DrawException as err:
            self.game_status = GameStatus.Draw
            print(err)
        except InvalidMoveException as invalidMove:
            self.winner = self.player2 if self.turn == self.player1.color else self.player1
            self.game_status = GameStatus.Win
            print(invalidMove)


    def moveGobblet(self, oldRow: int, oldColumn: int, newRow: int, newColumn: int):
        " Move already existent gobblet to new location "
        try:
            self.board.movePiece(oldRow, oldColumn, newRow, newColumn)
            self.__changeTurn()
        except DrawException as errDraw:
            self.game_status = GameStatus.Draw
            print(errDraw)
        except InvalidMovementSamePositionException as sameMoveExp:
            print(sameMoveExp)
        except InvalidMoveException as invalidMove:
            self.winner = self.player2 if self.turn == self.player1.color else self.player1
            self.game_status = GameStatus.Win
            print(invalidMove)

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


if __name__ == '__main__':
    pass
    # game = Game(GameModes.HumanVsHuman,"","",Color.WHITE,Color.BLACK)
    # game.game_status = GameStatus.Win
    # print(game.statusCheck())
    # game.moveGobblet(0,0,0,0)
    # game.moveGobblet(0,0,1,1)