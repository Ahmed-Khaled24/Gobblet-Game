import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('../src'))

from backend.board import Board
from backend.player import *
from utils.invalidMoveException import *


def test_createBoard():
    board = Board()
    assert isinstance(board, Board)

    
def test_addPieceToInvalidLocation():
    board = Board()
    piece = Piece(Color.BLACK, PieceSize.LARGE)
    with pytest.raises(AssertionError) as e:
        board.addPiece(5, 2, piece)
        
        
def test_addPieceToValidLocation():
    board = Board()
    piece = Piece(Color.BLACK, PieceSize.LARGE)
    try:
        board.addPiece(0, 0, piece)
    except AssertionError as e:
        pytest.fail("Unexpected assertion error raised: " + str(e))
    
    assert True
    
    
def test_addPieceOnTopOfSmallerOne():
    board = Board()
    large = Piece(Color.BLACK, PieceSize.LARGE)
    medium = Piece(Color.BLACK, PieceSize.MEDIUM)
    board.addPiece(0, 0, medium)
    try:
        board.addPiece(0, 0, large)
    except InvalidMoveException as e:
        pytest.fail("Unexpected InvalidMoveException raised: " + str(e))
    
    assert True
    
    
def test_addPieceOnTopOfBiggerOne():
    board = Board()
    large = Piece(Color.BLACK, PieceSize.LARGE)
    medium = Piece(Color.BLACK, PieceSize.MEDIUM)
    board.addPiece(0, 0, large)
    
    with pytest.raises(InvalidMoveException) as e:
        board.addPiece(0, 0, medium)
        

def test_validMovePiece():
    board = Board()
    large = Piece(Color.BLACK, PieceSize.LARGE)
    medium = Piece(Color.BLACK, PieceSize.MEDIUM)
    board.addPiece(0, 0, large)
    board.addPiece(0, 1, medium)
    
    board.movePiece(0, 0, 0, 1)
    
    assert board.grid[0][0][-1] is None
    assert board.grid[0][1][-1] is large
    assert board.grid[0][1][-2] is medium
    
    
def test_invalidMovePiece():
    board = Board()
    large = Piece(Color.BLACK, PieceSize.LARGE)
    medium = Piece(Color.BLACK, PieceSize.MEDIUM)
    board.addPiece(0, 0, large)
    board.addPiece(0, 1, medium)
    
    with pytest.raises(InvalidMoveException) as e:
        board.movePiece(0, 1, 0, 0)