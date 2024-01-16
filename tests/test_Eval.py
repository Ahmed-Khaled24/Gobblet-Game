from src.backend.Eval import *
from src.backend.player import *


def test_check_uniqueness():
    pieces1 = [Piece(Color.WHITE, PieceSize.LARGE),
               Piece(Color.WHITE, PieceSize.LARGE),
               Piece(Color.BLACK, PieceSize.LARGE)]

    pieces2 = [None] * 4
    pieces3 = [Piece(Color.WHITE, PieceSize.LARGE),
               Piece(Color.WHITE, PieceSize.LARGE),
               Piece(Color.WHITE, PieceSize.LARGE)]

    pieces4 = [Piece(Color.WHITE, PieceSize.LARGE),
               Piece(Color.WHITE, PieceSize.LARGE),
               None]
    pieces5 = pieces3 + pieces2
    assert Evaluation.check_uniqueness(pieces1) is False
    assert Evaluation.check_uniqueness(pieces2) is True
    assert Evaluation.check_uniqueness(pieces3) is True
    assert Evaluation.check_uniqueness(pieces4) is True
    assert Evaluation.check_uniqueness(pieces5) is True
