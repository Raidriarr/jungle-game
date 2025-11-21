import unittest

from jungle_game.model.board import Board, RIVER
from jungle_game.model.position import Position
from jungle_game.model.piece import Piece
from jungle_game.model.animal_type import ELEPHANT, LION, TIGER, LEOPARD, WOLF, DOG, CAT, RAT


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

    def test_only_rat_can_enter_river(self):
        board = make_empty_board()

        # land next to river; river at (3,1) in your layout
        land_pos = Position(3, 0)
        river_pos = Position(3, 1)

        # 1) Rat CAN enter river
        rat = Piece(RAT, 1, land_pos)
        board.pieces[land_pos.row][land_pos.col] = rat
        self.assertTrue(board.is_legal_move(rat, river_pos, 1))

        # clear the square
        board.pieces[land_pos.row][land_pos.col] = None

        # 2) All other animals CANNOT enter river
        other_types = [ELEPHANT, LION, TIGER, LEOPARD, WOLF, DOG, CAT]

        for animal_type in other_types:
            piece = Piece(animal_type, 1, land_pos)
            board.pieces[land_pos.row][land_pos.col] = piece

            self.assertFalse(
                board.is_legal_move(piece, river_pos, 1),
                msg=f"{animal_type.name} should NOT be able to enter river"
            )

            board.pieces[land_pos.row][land_pos.col] = None

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

    def test_lion_jump_blocked_by_rat_in_river(self):
        board = make_empty_board()

        # Lion on left bank, wants to jump horizontally across river.
        start = Position(3, 0)   # land
        end = Position(3, 6)     # land

        lion = Piece(LION, 1, start)
        board.pieces[start.row][start.col] = lion

        # Put a rat in the river in between
        rat_pos = Position(3, 2)  # this is a river tile
        rat = Piece(RAT, -1, rat_pos)
        board.pieces[rat_pos.row][rat_pos.col] = rat

        self.assertFalse(board.is_legal_move(lion, end, 1))

    def test_adjacent_land_move_is_legal(self):
        board = make_empty_board()

        start = Position(6, 0)
        target = Position(5, 0)

        dog = Piece(DOG, 1, start)
        board.pieces[start.row][start.col] = dog

        self.assertTrue(board.is_legal_move(dog, target, 1))

    def test_cannot_move_out_of_board(self):
        board = make_empty_board()

        start = Position(0, 0)
        cat = Piece(CAT, 1, start)
        board.pieces[start.row][start.col] = cat

        off_board_1 = Position(-1, 0)
        off_board_2 = Position(0, -1)

        self.assertFalse(board.is_inside(off_board_1))
        self.assertFalse(board.is_inside(off_board_2))
        self.assertFalse(board.is_legal_move(cat, off_board_1, 1))
        self.assertFalse(board.is_legal_move(cat, off_board_2, 1))

    def test_player1_cannot_enter_own_den(self):
        board = make_empty_board()

        # P1's den at (8,3); step from (8,2) -> (8,3)
        start = Position(8, 2)
        target = Position(8, 3)  # DEN_P1 according to your layout

        lion = Piece(LION, 1, start)
        board.pieces[start.row][start.col] = lion

        self.assertFalse(board.is_legal_move(lion, target, 1))

    def test_player2_cannot_enter_own_den(self):
        board = make_empty_board()

        # P2's den at (0,3); step from (0,2) -> (0,3)
        start = Position(0, 2)
        target = Position(0, 3)  # DEN_P2

        tiger = Piece(TIGER, -1, start)
        board.pieces[start.row][start.col] = tiger

        self.assertFalse(board.is_legal_move(tiger, target, -1))

    def test_can_enter_opponent_den(self):
        board = make_empty_board()

        # P1 moving into P2's den at (0,3) from (0,2)
        start = Position(0, 2)
        target = Position(0, 3)

        tiger = Piece(TIGER, 1, start)
        board.pieces[start.row][start.col] = tiger

        self.assertTrue(board.is_legal_move(tiger, target, 1))

    def test_lion_can_jump_over_clear_vertical_river(self):
        board = make_empty_board()

        start = Position(2, 1)  # land above river
        target = Position(6, 1)  # land below river

        lion = Piece(LION, 1, start)
        board.pieces[start.row][start.col] = lion

        self.assertTrue(board.is_legal_move(lion, target, 1))

    def test_tiger_can_jump_over_clear_vertical_river(self):
        board = make_empty_board()

        start = Position(2, 1)  # land above river
        target = Position(6, 1)  # land below river

        tiger = Piece(TIGER, 1, start)
        board.pieces[start.row][start.col] = tiger

        self.assertTrue(board.is_legal_move(tiger, target, 1))




if __name__ == "__main__":
    unittest.main()
