import unittest

from jungle_game.model.board import Board, RIVER
from jungle_game.model.position import Position
from jungle_game.model.piece import Piece
from jungle_game.model.animal_type import ELEPHANT, RAT, TIGER


def make_empty_board():
    """Helper: create a board with correct tiles but no pieces."""
    board = Board()
    for r in range(9):
        for c in range(7):
            board.pieces[r][c] = None
    return board


class TestBoardMovement(unittest.TestCase):
    def test_cannot_move_diagonally(self):
        board = make_empty_board()
        piece = Piece(RAT, 1, Position(4, 3))
        board.pieces[4][3] = piece

        target = Position(5, 4)  # diagonal
        self.assertFalse(board.is_legal_move(piece, target, 1))

    def test_rat_can_enter_river_but_elephant_cannot(self):
        board = make_empty_board()

        # river squares are in rows 3–5, cols 1–2 and 4–5.
        land_pos = Position(3, 0)
        river_pos = Position(3, 1)

        rat = Piece(RAT, 1, land_pos)
        elephant = Piece(ELEPHANT, 1, land_pos)

        # put only one piece at a time
        board.pieces[land_pos.row][land_pos.col] = rat
        self.assertTrue(board.is_legal_move(rat, river_pos, 1))

        board.pieces[land_pos.row][land_pos.col] = None
        board.pieces[land_pos.row][land_pos.col] = elephant
        self.assertFalse(board.is_legal_move(elephant, river_pos, 1))

    def test_tiger_jump_blocked_by_rat_in_river(self):
        board = make_empty_board()

        # Tiger on left bank, wants to jump horizontally across river.
        start = Position(3, 0)   # land
        end = Position(3, 6)     # land

        tiger = Piece(TIGER, 1, start)
        board.pieces[start.row][start.col] = tiger

        # Put a rat in the river in between
        rat_pos = Position(3, 2)  # this is a river tile
        rat = Piece(RAT, -1, rat_pos)
        board.pieces[rat_pos.row][rat_pos.col] = rat

        self.assertFalse(board.is_legal_move(tiger, end, 1))


if __name__ == "__main__":
    unittest.main()
