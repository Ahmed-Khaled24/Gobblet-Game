import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.'))
print(path)
sys.path.insert(0, path)

from time import sleep
from src.backend.game import Game, MoveType
from src.backend.player import Color
from src.utils.gameModesEnum import GameModes


if __name__ == '__main__':
    game = Game(GameModes.AiVsAi, "", "", Color.WHITE, Color.BLACK)
    while game.game_status == game.game_status.OnGame:
        playerInTurn = game.player1 if game.turn == game.player1.color else game.player2
        currentMove = game.getBestMove(playerInTurn)
        
        if currentMove.type == MoveType.ADD:
            game.addGobblet(currentMove.row, currentMove.column, currentMove.piece, currentMove.piece.externalStackIndex)
        else: 
            pass
        
        print(game.board.__str__())
        print('============================================================')
        # sleep(5)
    
    print(game.game_status, game.winner)
    