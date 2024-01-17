from src.backend.Eval import *
from src.backend.player import *


def test_check_uniqueness():
    pieces1 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.BLACK, PieceSize.LARGE),
    ]

    pieces2 = [None] * 4
    pieces3 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
    ]

    pieces4 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        None,
    ]
    pieces5 = pieces3 + pieces2
    assert Evaluation.check_uniqueness(pieces1) is False
    assert Evaluation.check_uniqueness(pieces2) is True
    assert Evaluation.check_uniqueness(pieces3) is True
    assert Evaluation.check_uniqueness(pieces4) is True
    assert Evaluation.check_uniqueness(pieces5) is True


def test_get_pieces_score():
    eval = Evaluation()
    board = Board()
    ai = AI(color=Color.WHITE)
    person = Person(color=Color.BLACK)
    eval.board, eval.max, eval.min = board, ai, person
    pieces1 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.BLACK, PieceSize.SMALL),
        None,
    ]

    pieces2 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.BLACK, PieceSize.LARGE),
        None,
    ]

    pieces3 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.BLACK, PieceSize.SMALL),
        Piece(Color.BLACK, PieceSize.SMALL),
    ]
    pieces4 = [
        Piece(Color.WHITE, PieceSize.LARGE),
        Piece(Color.WHITE, PieceSize.LARGE),
        None,
        None,
    ]
    pieces5 = [
        Piece(Color.BLACK, PieceSize.LARGE),
        Piece(Color.BLACK, PieceSize.LARGE),
        Piece(Color.BLACK, PieceSize.LARGE),
        None,
    ]
    assert eval.get_pieces_score(pieces1) == PieceSize.LARGE.value**2 * 10**2
    assert eval.get_pieces_score(pieces2) == 0
    assert eval.get_pieces_score(pieces3) == 0

    assert (
        eval.get_pieces_score(pieces4)
        == pieces4[0].size.value * 10 * pieces4[1].size.value * 10
    )
    assert eval.get_pieces_score(pieces5) == -1 * PieceSize.LARGE.value**3 * 10**3
