import unittest

from jungle_game.controller.game_controller import GameController
from jungle_game.model.game_state import GameState
from jungle_game.model.position import Position
from jungle_game.model.piece import Piece
from jungle_game.model.animal_type import RAT


def make_empty_controller():
    """
    Helper: create a controller with an empty board.
    """
    gs = GameState()

    # clear pieces
    for r in range(9):
        for c in range(7):
            gs.board.pieces[r][c] = None

    gs.current_player = 1
    gs.move_history = []
    gs.undo_used = {1: 0, -1: 0}
    gs.game_over = False

    return GameController(gs)


class TestGameController(unittest.TestCase):

    # --------------------------------------------------------
    # Basic construction
    # --------------------------------------------------------
    def test_new_game_creates_clean_state(self):
        ctrl = GameController.new_game()
        self.assertIsInstance(ctrl.game_state, GameState)
        self.assertEqual(ctrl.get_current_player(), 1)

    # --------------------------------------------------------
    # Board helpers
    # --------------------------------------------------------
    def test_get_board_size(self):
        ctrl = GameController.new_game()
        rows, cols = ctrl.get_board_size()
        self.assertEqual((rows, cols), (9, 7))

    def test_get_tile_type(self):
        ctrl = GameController.new_game()

        # Known tile: P2 den at (0,3)
        self.assertEqual(ctrl.get_tile_type(0, 3), "den2")

        # Known tile: a river tile (3,1)
        self.assertEqual(ctrl.get_tile_type(3, 1), "river")

    # --------------------------------------------------------
    # get_piece_name
    # --------------------------------------------------------
    def test_get_piece_name_none_when_empty(self):
        ctrl = make_empty_controller()
        self.assertIsNone(ctrl.get_piece_name(4, 4))

    def test_get_piece_name_returns_string(self):
        ctrl = make_empty_controller()

        pos = Position(4, 4)
        rat = Piece(RAT, 1, pos)
        ctrl.game_state.board.pieces[4][4] = rat

        name = ctrl.get_piece_name(4, 4)
        self.assertEqual(name.lower(), "rat")

    # --------------------------------------------------------
    # Selection rules
    # --------------------------------------------------------
    def test_can_select_piece_only_own_piece(self):
        ctrl = make_empty_controller()

        pos = Position(4, 4)
        rat1 = Piece(RAT, 1, pos)
        ctrl.game_state.board.pieces[4][4] = rat1

        pos2 = Position(2, 2)
        rat2 = Piece(RAT, -1, pos2)
        ctrl.game_state.board.pieces[2][2] = rat2

        ctrl.game_state.current_player = 1

        self.assertTrue(ctrl.can_select_piece(4, 4))  # own piece
        self.assertFalse(ctrl.can_select_piece(2, 2)) # enemy piece

    # --------------------------------------------------------
    # make_move
    # --------------------------------------------------------
    def test_make_move_call_delegates_to_game_state(self):
        ctrl = make_empty_controller()

        from_pos = Position(4, 4)
        to_pos   = Position(4, 5)

        rat = Piece(RAT, 1, from_pos)
        ctrl.game_state.board.pieces[4][4] = rat

        # Place an enemy piece so the board isn't empty after move
        ctrl.game_state.board.pieces[0][0] = Piece(RAT, -1, Position(0, 0))

        ok = ctrl.make_move(4, 4, 4, 5)
        self.assertTrue(ok)

        self.assertIs(ctrl.game_state.board.pieces[4][5], rat)

    # --------------------------------------------------------
    # undo
    # --------------------------------------------------------
    def test_undo_delegates_and_changes_state(self):
        ctrl = make_empty_controller()

        # simulate one move for undo to work
        from_pos = Position(4, 4)
        to_pos   = Position(4, 5)

        rat = Piece(RAT, 1, from_pos)
        ctrl.game_state.board.pieces[4][4] = rat
        ctrl.game_state.board.pieces[0][0] = Piece(RAT, -1, Position(0, 0))  # enemy present

        ctrl.make_move(4, 4, 4, 5)

        self.assertTrue(ctrl.undo())

        # rat returned to original square
        self.assertIs(ctrl.game_state.board.pieces[4][4], rat)

    # --------------------------------------------------------
    # save_game / load_game (serialization)
    # --------------------------------------------------------
    def test_save_and_load_game(self):
        import tempfile, os

        ctrl = make_empty_controller()

        # Add one custom piece
        pos = Position(4, 4)
        rat = Piece(RAT, 1, pos)
        ctrl.game_state.board.pieces[4][4] = rat

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jungle") as tmp:
            name = tmp.name
        
        try:
            ctrl.save_game(name)

            new_ctrl = GameController.new_game()
            new_ctrl.load_game(name)

            # the piece must appear in loaded state
            loaded = new_ctrl.get_piece_at(4, 4)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.animal_type.name, "Rat")

        finally:
            os.remove(name)

    # --------------------------------------------------------
    # replay_game
    # --------------------------------------------------------
    def test_replay_game_returns_move_list(self):
        import tempfile, os

        text = (
            "r1 c1 r2 c2 cap pl\n"
            "4 4 4 5 0 1\n"
            "4 5 4 6 0 1\n"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".record", mode="w") as tmp:
            tmp.write(text)
            name = tmp.name

        try:
            ctrl = GameController.new_game()
            moves = ctrl.replay_game(name)

            self.assertEqual(moves, [(4, 4, 4, 5), (4, 5, 4, 6)])

        finally:
            os.remove(name)


if __name__ == "__main__":
    unittest.main()