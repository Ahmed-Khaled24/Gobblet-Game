import pygame
from src.backend.AI import AI
from src.backend.game import Game
from src.utils.move import MoveType

class AiAgent:
    def __init__(self, game : Game):
        self.game = game
    
    def __get_current_player(self):
        return self.game.player1 if self.game.turn.value == self.game.player1.color.value else self.game.player2

    def on_turn(self, algorithm_type):
        player = self.__get_current_player()
        if player.difficulty == 2:
            pygame.time.delay(1000)
        print(f"Player: {player}")
        pygame.time.delay(100000)
        legal_action = self.game.getBestMove(player, algorithm_type)
        print(f"Legal Action: {legal_action}")
        if legal_action.type == MoveType.ADD:
            self.game.addGobblet(
                legal_action.row,
                legal_action.column,
                legal_action.piece,
                legal_action.piece.externalStackIndex,
            )
        elif legal_action.type == MoveType.MOVE:
            self.game.moveGobblet(
                oldRow=legal_action.piece.cur_pos[0],
                oldColumn=legal_action.piece.cur_pos[1],
                newRow=legal_action.row,
                newColumn=legal_action.column,
            )
