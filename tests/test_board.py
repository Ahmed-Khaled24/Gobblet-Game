import sys
import os
sys.path.insert(0, os.path.abspath('../src'))

import pytest
from src.backend.board import Board
from src.backend.player import *
from src.utils.invalidMoveException import *


def test_createBoard():
    board = Board()
    assert isinstance(board, Board)

    
def test_addPieceToInvalidLocation1():
    board = Board()
    piece = Piece(Color.BLACK, PieceSize.LARGE)
    with pytest.raises(AssertionError) as e:
        board.addPiece(5, 2, piece)
        
        
def test_addPieceToInvalidLocation1():
    board = Board()
    piece = Piece(Color.BLACK, PieceSize.LARGE)
    with pytest.raises(AssertionError) as e:
        board.addPiece(0, 5, piece)
        
        
def test_addPieceToValidLocation1():
    board = Board()
    piece = Piece(Color.BLACK, PieceSize.LARGE)
    try:
        board.addPiece(0, 0, piece)
    except AssertionError as e:
        pytest.fail("Unexpected assertion error raised: " + str(e))
    
    assert True
 
    
def test_addPieceToValidLocation2():
    board = Board()
    piece = Piece(Color.BLACK, PieceSize.LARGE)
    try:
        board.addPiece(3, 3, piece)
    except AssertionError as e:
        pytest.fail("Unexpected assertion error raised: " + str(e))
    
    assert True
    
            
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
        

def test_getLinedUpGobblets():
    board = Board()
    board.addPiece(0, 0, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(0, 1, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(0, 2, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(0, 3, Piece(Color.BLACK, PieceSize.LARGE))
    
    board.addPiece(1, 0, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(1, 1, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(1, 2, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(1, 3, Piece(Color.BLACK, PieceSize.LARGE))
    
    board.addPiece(2, 0, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(2, 1, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(2, 2, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(2, 3, Piece(Color.BLACK, PieceSize.LARGE))
    
    board.addPiece(3, 0, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(3, 1, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(3, 2, Piece(Color.BLACK, PieceSize.LARGE))
    board.addPiece(3, 3, Piece(Color.BLACK, PieceSize.LARGE))
    
    result = board.getLinedUpGobblets(Color.BLACK)
    
    assert result == [
        [(0,0), (0,1), (0,2), (0,3)], 
        [(1,0), (1,1), (1,2), (1,3)], 
        [(2,0), (2,1), (2,2), (2,3)], 
        [(3,0), (3,1), (3,2), (3,3)], 
        [(0,0), (1,0), (2,0), (3,0)],
        [(0,1), (1,1), (2,1), (3,1)],
        [(0,2), (1,2), (2,2), (3,2)],
        [(0,3), (1,3), (2,3), (3,3)],
        [(2, 0), (1, 1), (0, 2)],
        [(3,0),(2,1), (1,2), (0,3)],
        [(3, 1), (2, 2), (1, 3)],
        [(1, 0), (2, 1), (3, 2)],
        [(0,0), (1,1), (2,2), (3,3)],
        [(0, 1), (1, 2), (2, 3)],
    ] 


def test_addPieceOnTopOfSmallerOne1():
    board = Board()
    board.addPiece(0, 0, Piece(Color.BLACK, PieceSize.MEDIUM))
    board.addPiece(0, 1, Piece(Color.BLACK, PieceSize.MEDIUM))
    board.addPiece(0, 2, Piece(Color.BLACK, PieceSize.MEDIUM))
    try:
        board.addPiece(0, 0, Piece(Color.WHITE, PieceSize.LARGE))
    except InvalidMoveException as e:
        pytest.fail("Unexpected InvalidMoveException raised: " + str(e))
    
    assert True
   
    
def test_addPieceOnTopOfSmallerOne2():
    board = Board()
    board.addPiece(0, 0, Piece(Color.BLACK, PieceSize.MEDIUM))
    board.addPiece(0, 1, Piece(Color.BLACK, PieceSize.MEDIUM))
    
    with pytest.raises(InvalidMoveException) as e:
        board.addPiece(0, 0, Piece(Color.WHITE, PieceSize.LARGE))
    
    
    
# def test_addPieceOnTopOfBiggerOne():
#     board = Board()
#     large = Piece(Color.BLACK, PieceSize.LARGE)
#     medium = Piece(Color.BLACK, PieceSize.MEDIUM)
#     board.addPiece(0, 0, large)
    
#     with pytest.raises(InvalidMoveException) as e:
#         board.addPiece(0, 0, medium)