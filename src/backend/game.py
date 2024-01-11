from copy import deepcopy
from enum import Enum
from typing import Tuple, Optional

from src.backend.Board import Board
from src.backend.Person import *
from src.utils.drawException import DrawException
from src.backend.AI import AI
from src.utils.invalidMoveException import (
    InvalidMoveException,
    InvalidMovementSamePositionException,
)
from src.utils.move import Move, MoveType
from src.utils.piece import Piece


class GameStatus(Enum):
    Win = 1
    Draw = 2
    OnGame = 3

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class GameModes(Enum):
    HumanVsHuman: int = 0
    HumanVsAi: int = 1
    AiVsAi: int = 2

    def __eq__(self, other):
        if isinstance(other, GameModes):
            return self.value == other.value
        return NotImplemented


class Game:
    def __init__(
        self,
        mode: GameModes,
        player1Name: str,
        player2Name: str,
        player1Color: Color,
        player2Color: Color,
    ):
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

    def __changeTurn(self) -> None:
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        else:
            self.turn = Color.WHITE

    # 0 <= row <4
    # 0 <= Col <4
    # 0 <= external_row < 3
    def addGobblet(
        self,
        row: int,
        column: int,
        piece: Piece,
        external_row: int,
        isVirtualMove: bool = False,
    ):
        "Add gobblet from the external stack"
        try:
            if piece.color == self.player1.color:
                self.board.addPiece(
                    row, column, piece, self.player1, external_row, isVirtualMove
                )
            else:
                self.board.addPiece(
                    row, column, piece, self.player2, external_row, isVirtualMove
                )
            self.__changeTurn()
            self.winState()
        except DrawException as err:
            self.game_status = GameStatus.Draw
            print(err)
        except InvalidMoveException as invalidMove:
            self.winner = (
                self.player2 if self.turn == self.player1.color else self.player1
            )
            self.game_status = GameStatus.Win
            print(invalidMove)

    def moveGobblet(self, oldRow: int, oldColumn: int, newRow: int, newColumn: int):
        "Move already existent gobblet to new location"
        try:
            self.board.movePiece(oldRow, oldColumn, newRow, newColumn)
            self.__changeTurn()
            self.winState()
        except DrawException as errDraw:
            self.game_status = GameStatus.Draw
            print(errDraw)
        except InvalidMovementSamePositionException as sameMoveExp:
            print(sameMoveExp)
        except InvalidMoveException as invalidMove:
            self.winner = (
                self.player2 if self.turn == self.player1.color else self.player1
            )
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
            self.winner = (
                self.player1 if self.player1.color == Color.WHITE else self.player2
            )
            self.game_status = GameStatus.Win
        elif len(black) > 0:
            self.winner = (
                self.player1 if self.player1.color == Color.BLACK else self.player2
            )
            self.game_status = GameStatus.Win

    def __getAvailableMoves(self, currentBoard: Board, currentPlayer: AI) -> list[Move]:
        """
        Returns a list of all possible moves for the current player.
        NOTE: This function currently only checks for the empty cells on the board and return moves for adding a piece from the external stack.
        We need to add the moves for moving a piece on the board. or adding piece from external stack on top of another piece.
        I believe اننا نمشي نفسنا كده و خلاص
        """
        moves = []
        piece: Piece = None
        for row in currentPlayer.pieces:  # Trivial way to get the piece to play
            if len(row) > 0:
                piece = row[-1]
                break

        for row in range(4):
            for column in range(4):
                if currentBoard.grid[row][column][-1] is None:
                    moves.append(
                        Move(MoveType.ADD, piece, row, column, piece.externalStackIndex)
                    )

        return moves

    def __makeMove(self, currentBoard: Board, move: Move) -> Board:
        """This function creates a deep copy of the current board and makes the given move on the copy.
        then return the new board to perform the minimax algorithm on it."""
        assert move is not None
        assert currentBoard is not None
        
        newBoard = deepcopy(currentBoard)
        if move.type == MoveType.ADD:
            currentPlayer = (
                self.player1 if move.piece.color == self.player1.color else self.player2
            )
            newBoard.addPiece(
                move.row,
                move.column,
                move.piece,
                currentPlayer,
                move.piece.externalStackIndex,
                isVirtualMove=True,
            )
        ## if we handle the move piece, we need to add extra code here but نمشي نفسنا
        return newBoard

    def __evaluate(self, board: Board, player: AI) -> int:
        """
        This is the static evaluation function (heuristic) for the minimax algorithm.
        It returns a number that represents the score of the current board state for the given player.
        The higher the number, the better the move is for the player. The lower the number,
        the worse the board is for the player.
        The algorithm used here is a trivial one. You can improve it to get better results.
        Add points for each piece the player has on the board, and subtract points for each piece the opponent has on the board.
        Possible improvements:
            1. Add more points if the AI has three pieces in a row, column, or diagonal
            2. Subtract more points if the opponent has three pieces in a row, column, or diagonal
        """
        score = 0
        for row in board.grid:
            for cell in row:
                piece = cell[-1]
                if piece is None:
                    continue
                if piece.color == player.color:
                    score += 1
                else:
                    score -= 1

        return score

    def __minimax(
        self, currentBoard: Board, currentPlayer: AI, maxDepth: int, currentDepth: int
    ) -> Tuple[int, Move]:
        """This function is the minimax algorithm. It returns the best move for the given player."""

        ## Base case
        possibleMoves = self.__getAvailableMoves(currentBoard, currentPlayer) ## If this returns empty list then this is a terminal state.
        if currentDepth == maxDepth or len(possibleMoves) == 0:
            return self.__evaluate(currentBoard, currentPlayer), None

        ## Bubble up the best move
        bestMove = None
        bestScore = -10e12 if currentPlayer.color == self.turn else 10e12
        for move in possibleMoves:
            newBoard = self.__makeMove(currentBoard, move)
            nextPlayer = (
                self.player1
                if currentPlayer.color == self.player2.color
                else self.player2
            )
            currentScore, currentMove = self.__minimax(
                newBoard, nextPlayer, maxDepth, currentDepth + 1
            )
            if currentPlayer.color == self.turn:  # Maximizing player
                if currentScore > bestScore:
                    bestScore = currentScore
                    bestMove = move
            else:  # Minimizing player
                if currentScore < bestScore:
                    bestScore = currentScore
                    bestMove = move

        return bestScore, bestMove

    def getBestMove(self, player: AI) -> Move:
        """This function is the interface for the minimax algorithm."""
        score, move = self.__minimax(
            self.board, player, player.difficulty, 0
        )  # maxDepth is the difficulty level
        print(f'Best move is: {move} with score: {score}')
        return move


if __name__ == "__main__":
    pass
