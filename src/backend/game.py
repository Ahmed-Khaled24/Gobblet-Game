from copy import deepcopy
from enum import Enum
import math
from typing import Tuple, Optional
from src.backend.board import Board
from src.backend.Person import *
from src.backend.player import Player
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
    MIN = 0
    MAX = 1

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
            self.player2 = AI(player2Color, player2Name)
        elif mode == GameModes.AiVsAi:
            self.player1 = AI(player1Color, player1Name)
            self.player2 = AI(player2Color, player2Name)
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

    def get_top_pieces(self, player: AI) -> list[Piece]:
        """ Returns the pieces on the top of each stack """
        possible_outsides = []
        for stack in player.pieces:
            if stack and len(stack) > 0:
                possible_outsides.append(stack[-1])  # The last piece in the list is on the top of the stack
        return possible_outsides

    def __getAvailableMoves(self, currentBoard: Board, currentPlayer: AI) -> list[Move]:
        """
        Returns a list of all possible moves for the current player.
        The list contains all possible addPiece and movePiece actions.
        """
        moves = []
        piece: Piece = None

        # get the largest piece in the external stack of the current user 
        largestPiece = None
        topPieces = self.get_top_pieces(currentPlayer)
        size = -1
        for piece in topPieces:
            if piece.size.value > size:
                size = piece.size.value
                largestPiece = piece
        # if the largest piece is None then there is no available pieces in 
        # the external stacks - add piece actions - and we need to check movePiece actions
        if largestPiece is not None:
            for row in range(4):
                for column in range(4):
                    # if the cell is empty then we can add the largest piece to it
                    if currentBoard.grid[row][column][-1] is None:
                        moves.append(
                            Move(MoveType.ADD, largestPiece, row, column, largestPiece.externalStackIndex)
                        )
                    # if the cell is not empty then we need to check if we can add the largest piece on top of it
                    else:
                        try:
                            # try to make the add action on a clone board 
                            # if it raises an exception then it is not a valid move
                            boardClone = deepcopy(currentBoard)
                            boardClone.addPiece(row, column, largestPiece, currentPlayer,
                                                largestPiece.externalStackIndex, isVirtualMove=True)
                            moves.append(
                                Move(MoveType.ADD, largestPiece, row, column, largestPiece.externalStackIndex)
                            )
                        except Exception:
                            pass

        ## Try all of them using movePiece function 
        ## and if it raises an exception then it is not a valid move
        for row in range(4):
            for column in range(4):
                current_piece = currentBoard.grid[row][column][-1]

                if current_piece is None:
                    continue
                if current_piece.color != currentPlayer.color:
                    continue

                for row2 in range(4):
                    for column2 in range(4):

                        try:
                            boardClone = deepcopy(currentBoard)
                            boardClone.movePiece(row, column, row2, column2, isVirtualMove=True)
                            moves.append(
                                Move(
                                    MoveType.MOVE,
                                    current_piece,
                                    row2,
                                    column2,
                                    None
                                )
                            )


                        except Exception:
                            pass

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

    def alpha_beta_recursion(self, curr_depth, agent_turn, currentPlayer, currentBoard, alpha, beta):
        if curr_depth == 0:  # reached a leaf  or  finished game
            return self.__evaluate(currentBoard, currentPlayer)
        possibleMoves = self.__getAvailableMoves(currentBoard, currentPlayer)

        if agent_turn == self.MAX:
            for legal_action in possibleMoves:
                newBoard = self.__makeMove(currentBoard, legal_action)
                nextPlayer = (
                    self.player1
                    if currentPlayer.color == self.player2.color
                    else self.player2
                )
                curr_score = self.alpha_beta_recursion(curr_depth - 1, self.MIN, nextPlayer, newBoard, alpha, beta)
                if beta <= alpha:
                    break
                alpha = max(alpha, curr_score)
            return alpha

        else:  # MIN
            for legal_action in possibleMoves:
                newBoard = self.__makeMove(currentBoard, legal_action)
                nextPlayer = (
                    self.player1
                    if currentPlayer.color == self.player2.color
                    else self.player2
                )
                curr_score = self.alpha_beta_recursion(curr_depth - 1, self.MAX, nextPlayer, newBoard, alpha, beta)
                if beta <= alpha:
                    break
                beta = min(beta, curr_score)
            return beta

    def get_action(
            self, currentBoard: Board, currentPlayer: AI, maxDepth: int) -> Tuple[int, Move]:

        actions_scores = []
        possibleMoves = self.__getAvailableMoves(currentBoard, currentPlayer)
        for legal_action in possibleMoves:
            newBoard = self.__makeMove(currentBoard, legal_action)
            nextPlayer = (
                self.player1
                if currentPlayer.color == self.player2.color
                else self.player2
            )
            score = self.alpha_beta_recursion(maxDepth - 1, self.MIN, nextPlayer, newBoard, alpha=-10e12,
                                              beta=10e12)
            actions_scores.append((legal_action, score))
        just_scores = [score for _, score in actions_scores]
        best_score = max(just_scores)
        best_actions = [action for action, score in actions_scores if score == best_score]
        return best_score, best_actions[0]

    def __minimax(
            self, currentBoard: Board, currentPlayer: AI, maxDepth: int, currentDepth: int
    ) -> Tuple[int, Move]:
        """This function is the minimax algorithm. It returns the best move for the given player."""

        ## Base case
        possibleMoves = self.__getAvailableMoves(currentBoard,
                                                 currentPlayer)  ## If this returns empty list then this is a terminal state.
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

    def getBestMove(self, player: AI, TYPE) -> Move:
        """This function is the interface for the minimax algorithm."""
        if TYPE == 1:
            score, move = self.__minimax(
                self.board, player, player.difficulty, 0)  # maxDepth is the difficulty level
            print(f'Best move is: {move} with score: {score}')
            return move
        if TYPE == 2:
            score, move = self.get_action(
                self.board, player, player.difficulty)  # maxDepth is the difficulty level
            print(f'Best move is: {move} with score: {score}')
            return move


if __name__ == "__main__":
    pass
