import pytest

from src.backend.player import *


def test_update_pos():
    p = Piece(Color.WHITE, PieceSize.LARGE)
    p.prev_pos = (1, 1)
    p.cur_pos = (1, 2)
    try:
        p.update_pos((1, 1))
    except DrawException as ex:
        assert False, f"{ex}"
    p.update_pos((1, 2))
    assert p.counter_for_draw == 2

    p.update_pos((1, 1))
    p.update_pos((1, 2))
    assert p.counter_for_draw == 4
    p.update_pos((1, 1))
    with pytest.raises(DrawException):
        p.update_pos((1, 2))
