
import pytest

from src.backend.game import Game
from src.backend.player import *
from src.utils.gameModesEnum import *
from src.backend.board import Board

def test_checkWinState1():
    game = Game(GameModes.HumanVsHuman, "Player1", "Player2", Color.WHITE, Color.BLACK)
    
    game.addGobblet(0, 0, Piece(Color.WHITE, PieceSize.LARGE))
    game.addGobblet(0, 1, Piece(Color.WHITE, PieceSize.LARGE))
    game.addGobblet(0, 2, Piece(Color.WHITE, PieceSize.LARGE))
    game.addGobblet(0, 3, Piece(Color.WHITE, PieceSize.LARGE))
    
    assert game.winState() == game.player1
    
def test_checkWinState2():
    game = Game(GameModes.HumanVsHuman, "Player1", "Player2", Color.WHITE, Color.BLACK)
    
    game.addGobblet(0, 0, Piece(Color.BLACK, PieceSize.LARGE))
    game.addGobblet(0, 1, Piece(Color.BLACK, PieceSize.LARGE))
    game.addGobblet(0, 2, Piece(Color.BLACK, PieceSize.LARGE))
    game.addGobblet(0, 3, Piece(Color.BLACK, PieceSize.LARGE))
    
    assert game.winState() == game.player2
    
def test_checkWinState3():
    game = Game(GameModes.HumanVsHuman, "Player1", "Player2", Color.WHITE, Color.BLACK)
    
    game.addGobblet(0, 0, Piece(Color.WHITE, PieceSize.LARGE))
    game.addGobblet(1, 1, Piece(Color.WHITE, PieceSize.LARGE))
    game.addGobblet(2, 2, Piece(Color.WHITE, PieceSize.LARGE))
    game.addGobblet(3, 3, Piece(Color.WHITE, PieceSize.LARGE))
    
    assert game.winState() == game.player1
    
def test_checkWinState4():
    game = Game(GameModes.HumanVsHuman, "Player1", "Player2", Color.WHITE, Color.BLACK)
    
    assert game.winState() == None