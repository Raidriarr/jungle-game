import unittest

from jungle_game.model.game_state import GameState
from jungle_game.model.board import Board
from jungle_game.model.position import Position
from jungle_game.model.piece import Piece
from jungle_game.model.animal_type import RAT, CAT


def make_simple_state():
    """
    Create a GameState with an empty board and
    two pieces in simple positions for undo testing.
    """
    gs = GameState()

    # clear the initial pieces
    for r in range(9):
        for c in range(7):
            gs.board.pieces[r][c] = None

    # place P1 rat at (6, 0), P2 cat at (5, 0)
    rat_pos = Position(6, 0)
    cat_pos = Position(5, 0)

    rat = Piece(RAT, 1, rat_pos)
    cat = Piece(CAT, -1, cat_pos)

    gs.board.pieces[6][0] = rat
    gs.board.pieces[5][0] = cat

    gs.current_player = 1

    return gs, rat_pos, cat_pos


class TestGameState(unittest.TestCase):
    def test_undo_restores_positions_and_turn(self):
        gs, rat_pos, cat_pos = make_simple_state()

        # P1 moves rat to capture cat
        move_ok = gs.make_move(rat_pos, cat_pos)
        self.assertTrue(move_ok)

        # after move: rat should be at cat_pos, cat gone
        self.assertIsNotNone(gs.board.pieces[cat_pos.row][cat_pos.col])
        self.assertEqual(gs.board.pieces[cat_pos.row][cat_pos.col].player, 1)
        self.assertIsNone(gs.board.pieces[rat_pos.row][rat_pos.col])

        # current player should now be -1
        self.assertEqual(gs.current_player, -1)

        # undo last move
        undone = gs.undo_last_move()
        self.assertTrue(undone)

        # rat back to original square
        self.assertIsNotNone(gs.board.pieces[rat_pos.row][rat_pos.col])
        self.assertEqual(gs.board.pieces[rat_pos.row][rat_pos.col].player, 1)

        # cat restored
        self.assertIsNotNone(gs.board.pieces[cat_pos.row][cat_pos.col])
        self.assertEqual(gs.board.pieces[cat_pos.row][cat_pos.col].player, -1)

        # current player back to 1
        self.assertEqual(gs.current_player, 1)


if __name__ == "__main__":
    unittest.main()
