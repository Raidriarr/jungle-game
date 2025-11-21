import unittest

from jungle_game.model.game_state import GameState
from jungle_game.model.position import Position
from jungle_game.model.piece import Piece
from jungle_game.model.animal_type import RAT, LION, TIGER


def make_empty_state():
    """
    Helper: create a GameState with correct tiles but NO pieces.
    Also reset flags so each test starts from a clean situation.
    """
    gs = GameState()

    # remove all initial pieces
    for r in range(9):
        for c in range(7):
            gs.board.pieces[r][c] = None

    gs.current_player = 1
    gs.game_over = False
    gs.winner = None
    gs.move_history = []
    gs.undo_used = {1: 0, -1: 0}
    return gs


def make_simple_state():
    """
    Helper used for undo & capture tests.

    Board:
    - P1 rat at (6,0)
    - P2 rat at (5,0)
    P1 to move.
    """
    gs = make_empty_state()

    rat_pos = Position(6, 0)
    enemy_pos = Position(5, 0)

    rat1 = Piece(RAT, 1, rat_pos)
    rat2 = Piece(RAT, -1, enemy_pos)

    gs.board.pieces[6][0] = rat1
    gs.board.pieces[5][0] = rat2

    gs.current_player = 1

    return gs, rat_pos, enemy_pos


class TestGameState(unittest.TestCase):

    # ------------------------------------------------------------------
    # Basic state & helpers
    # ------------------------------------------------------------------
    def test_initial_state_basic_flags(self):
        gs = GameState()
        self.assertEqual(gs.current_player, 1)
        self.assertFalse(gs.game_over)
        self.assertIsNone(gs.winner)
        self.assertEqual(gs.undo_used, {1: 0, -1: 0})
        self.assertIsInstance(gs.board, type(gs.board))
        self.assertEqual(len(gs.move_history), 0)

    # ------------------------------------------------------------------
    # make_move: invalid cases
    # ------------------------------------------------------------------
    def test_make_move_fails_if_game_over(self):
        gs, from_pos, to_pos = make_simple_state()
        gs.game_over = True
        self.assertFalse(gs.make_move(from_pos, to_pos))

    def test_make_move_fails_if_no_piece_on_from(self):
        gs = make_empty_state()
        from_pos = Position(3, 3)
        to_pos = Position(3, 4)
        self.assertFalse(gs.make_move(from_pos, to_pos))

    def test_make_move_fails_if_piece_belongs_to_other_player(self):
        gs = make_empty_state()
        from_pos = Position(3, 3)
        to_pos = Position(3, 4)

        enemy = Piece(RAT, -1, from_pos)
        gs.board.pieces[3][3] = enemy
        gs.current_player = 1

        self.assertFalse(gs.make_move(from_pos, to_pos))

    # ------------------------------------------------------------------
    # make_move: normal non-winning move
    # ------------------------------------------------------------------
    def test_make_move_normal_switches_player_and_records_history(self):
        gs = make_empty_state()

        from_pos = Position(4, 3)
        to_pos = Position(4, 4)

        p1_rat = Piece(RAT, 1, from_pos)
        gs.board.pieces[4][3] = p1_rat

        # put one enemy piece somewhere so game is not over by elimination
        enemy_pos = Position(0, 0)
        gs.board.pieces[0][0] = Piece(RAT, -1, enemy_pos)

        ok = gs.make_move(from_pos, to_pos)
        self.assertTrue(ok)

        # piece moved
        self.assertIs(gs.board.pieces[4][4], p1_rat)
        self.assertIsNone(gs.board.pieces[4][3])
        self.assertEqual(p1_rat.position, to_pos)

        # player switched
        self.assertEqual(gs.current_player, -1)

        # history recorded
        self.assertEqual(len(gs.move_history), 1)
        h_from, h_to, h_captured, h_player = gs.move_history[-1]
        self.assertEqual(h_from, from_pos)
        self.assertEqual(h_to, to_pos)
        self.assertIsNone(h_captured)
        self.assertEqual(h_player, 1)

        # no winner yet
        self.assertFalse(gs.game_over)
        self.assertIsNone(gs.winner)

    # ------------------------------------------------------------------
    # make_move: win by entering the opponent's den
    # board layout: P2 den is at (0,3), P1 den is at (8,3)
    # ------------------------------------------------------------------
    def test_make_move_win_by_entering_p2_den(self):
        gs = make_empty_state()

        from_pos = Position(1, 3)
        to_pos = Position(0, 3)  # DEN_P2

        attacker = Piece(RAT, 1, from_pos)
        gs.board.pieces[1][3] = attacker

        # have at least one enemy piece somewhere (not actually needed,
        # but makes it clear this is a den-win, not elimination)
        gs.board.pieces[2][0] = Piece(RAT, -1, Position(2, 0))

        ok = gs.make_move(from_pos, to_pos)
        self.assertTrue(ok)
        self.assertTrue(gs.game_over)
        self.assertEqual(gs.winner, 1)

        # current player should NOT change after win
        self.assertEqual(gs.current_player, 1)

    def test_make_move_win_by_entering_p1_den(self):
        gs = make_empty_state()
        gs.current_player = -1

        from_pos = Position(7, 3)
        to_pos = Position(8, 3)  # DEN_P1

        attacker = Piece(RAT, -1, from_pos)
        gs.board.pieces[7][3] = attacker

        gs.board.pieces[6][0] = Piece(RAT, 1, Position(6, 0))

        ok = gs.make_move(from_pos, to_pos)
        self.assertTrue(ok)
        self.assertTrue(gs.game_over)
        self.assertEqual(gs.winner, -1)
        self.assertEqual(gs.current_player, -1)

    # ------------------------------------------------------------------
    # make_move: win by eliminating all opponent pieces
    # ------------------------------------------------------------------
    def test_make_move_win_by_eliminating_last_enemy_piece(self):
        """
        Only one enemy piece on the board; capturing it should end the game.
        """
        gs, rat_pos, enemy_pos = make_simple_state()

        ok = gs.make_move(rat_pos, enemy_pos)
        self.assertTrue(ok)

        self.assertTrue(gs.game_over)
        self.assertEqual(gs.winner, 1)
        # after game over, player should not switch
        self.assertEqual(gs.current_player, 1)

    # ------------------------------------------------------------------
    # can_undo
    # ------------------------------------------------------------------
    def test_can_undo_false_when_no_history(self):
        gs = GameState()
        self.assertFalse(gs.can_undo(1))

    def test_can_undo_false_when_game_over(self):
        gs = GameState()
        gs.game_over = True
        self.assertFalse(gs.can_undo(1))

    def test_can_undo_false_when_last_move_other_player(self):
        gs = GameState()
        gs.move_history.append((Position(0, 0), Position(0, 1), None, -1))
        self.assertFalse(gs.can_undo(1))

    def test_can_undo_false_when_used_three_times(self):
        gs = GameState()
        gs.move_history.append((Position(0, 0), Position(0, 1), None, 1))
        gs.undo_used[1] = 3
        self.assertFalse(gs.can_undo(1))

    def test_can_undo_true_normal_case(self):
        gs = GameState()
        gs.move_history.append((Position(0, 0), Position(0, 1), None, 1))
        gs.undo_used[1] = 1
        self.assertTrue(gs.can_undo(1))

    # ------------------------------------------------------------------
    # undo_last_move (using our simple state helper)
    # ------------------------------------------------------------------
    def test_undo_restores_positions_and_turn(self):
        """
        P1 rat captures P2 rat (last enemy piece, so game ends),
        then we undo. Positions, player turn and undo counter should reset.
        """
        gs, rat_pos, enemy_pos = make_simple_state()

        # P1 moves rat to capture enemy rat (this is last enemy piece)
        move_ok = gs.make_move(rat_pos, enemy_pos)
        self.assertTrue(move_ok)

        # after move: attacker at enemy_pos, original square empty
        self.assertIsNotNone(gs.board.pieces[enemy_pos.row][enemy_pos.col])
        self.assertEqual(gs.board.pieces[enemy_pos.row][enemy_pos.col].player, 1)
        self.assertIsNone(gs.board.pieces[rat_pos.row][rat_pos.col])

        # game ended by elimination, so current player stays 1
        self.assertTrue(gs.game_over)
        self.assertEqual(gs.winner, 1)
        self.assertEqual(gs.current_player, 1)

        # undo last move
        undone = gs.undo_last_move()
        self.assertTrue(undone)

        # rat back to original square
        self.assertIsNotNone(gs.board.pieces[rat_pos.row][rat_pos.col])
        self.assertEqual(gs.board.pieces[rat_pos.row][rat_pos.col].player, 1)

        # enemy rat restored
        self.assertIsNotNone(gs.board.pieces[enemy_pos.row][enemy_pos.col])
        self.assertEqual(gs.board.pieces[enemy_pos.row][enemy_pos.col].player, -1)

        # current player back to 1
        self.assertEqual(gs.current_player, 1)
        # undo counter increased for player 1
        self.assertEqual(gs.undo_used[1], 1)

    def test_undo_reverts_game_over_and_winner_and_captured_piece(self):
        """
        P1 captures the last P2 piece (elimination win), then undo.
        Game should no longer be over, winner None, and the captured
        piece should be alive and back on the board.
        """
        gs, rat_pos, enemy_pos = make_simple_state()

        # defender reference BEFORE move
        defender = gs.board.pieces[enemy_pos.row][enemy_pos.col]
        self.assertEqual(defender.player, -1)

        # capture last enemy -> win by elimination
        ok = gs.make_move(rat_pos, enemy_pos)
        self.assertTrue(ok)
        self.assertTrue(gs.game_over)
        self.assertEqual(gs.winner, 1)

        # defender is now dead (removed from board but object exists)
        self.assertFalse(defender.alive)

        # undo the move
        undone = gs.undo_last_move()
        self.assertTrue(undone)

        # attacker back to original square
        attacker = gs.board.pieces[rat_pos.row][rat_pos.col]
        self.assertIsNotNone(attacker)
        self.assertEqual(attacker.player, 1)

        # defender back on its original square and alive again
        self.assertIs(gs.board.pieces[enemy_pos.row][enemy_pos.col], defender)
        self.assertTrue(defender.alive)

        # game flags reset
        self.assertFalse(gs.game_over)
        self.assertIsNone(gs.winner)
        self.assertEqual(gs.current_player, 1)
        self.assertEqual(gs.undo_used[1], 1)

    def test_undo_last_move_returns_false_if_no_history(self):
        gs = GameState()
        self.assertFalse(gs.undo_last_move())

    # ------------------------------------------------------------------
    # get_legal_moves
    # ------------------------------------------------------------------
    def test_get_legal_moves_returns_only_moves_for_that_player(self):
        gs = make_empty_state()

        p1_pos = Position(4, 3)
        p2_pos = Position(2, 2)

        p1 = Piece(RAT, 1, p1_pos)
        p2 = Piece(RAT, -1, p2_pos)

        gs.board.pieces[p1_pos.row][p1_pos.col] = p1
        gs.board.pieces[p2_pos.row][p2_pos.col] = p2

        moves_p1 = gs.get_legal_moves(1)
        for frm, to in moves_p1:
            piece = gs.board.get_piece(frm)
            self.assertEqual(piece.player, 1)

        moves_p2 = gs.get_legal_moves(-1)
        for frm, to in moves_p2:
            piece = gs.board.get_piece(frm)
            self.assertEqual(piece.player, -1)

    def test_get_legal_moves_includes_jump_for_lion(self):
        """
        Row 3 in your board:
        [LAND, RIVER, RIVER, LAND, RIVER, RIVER, LAND]

        Put Lion at (3,0). Legal moves for that lion should include (3,3),
        which is the 'jump over river' move.
        """
        gs = make_empty_state()

        start = Position(3, 0)
        lion = Piece(LION, 1, start)
        gs.board.pieces[3][0] = lion

        moves = gs.get_legal_moves(1)
        as_tuples = {(frm.row, frm.col, to.row, to.col) for frm, to in moves}

        self.assertIn((3, 0, 3, 3), as_tuples)

    # ------------------------------------------------------------------
    # Serialization: to_dict / from_dict
    # ------------------------------------------------------------------
    def test_to_dict_has_expected_keys(self):
        gs = GameState()
        data = gs.to_dict()

        self.assertIn("current_player", data)
        self.assertIn("undo_used", data)
        self.assertIn("pieces", data)

    def test_serialization_roundtrip_recreates_board_and_meta(self):
        """
        Modify a few fields, serialize, then recreate a new GameState
        using from_dict and check if they match.
        """
        gs = GameState()
        gs.current_player = -1
        gs.undo_used[1] = 2
        gs.undo_used[-1] = 1

        # move one piece to make sure layout is not purely initial
        orig_pos = Position(8, 0)
        new_pos = Position(7, 0)
        piece = gs.board.get_piece(orig_pos)
        if piece is not None:
            gs.board.pieces[orig_pos.row][orig_pos.col] = None
            gs.board.pieces[new_pos.row][new_pos.col] = piece
            piece.position = new_pos

        data = gs.to_dict()
        gs2 = GameState.from_dict(data)

        self.assertEqual(gs2.current_player, -1)
        self.assertEqual(gs2.undo_used[1], 2)
        self.assertEqual(gs2.undo_used[-1], 1)

        # check pieces
        for r in range(9):
            for c in range(7):
                p1 = gs.board.pieces[r][c]
                p2 = gs2.board.pieces[r][c]

                if p1 is None:
                    self.assertIsNone(p2)
                else:
                    self.assertIsNotNone(p2)
                    self.assertEqual(p1.animal_type.name, p2.animal_type.name)
                    self.assertEqual(p1.player, p2.player)
                    self.assertEqual(p2.position.row, r)
                    self.assertEqual(p2.position.col, c)


if __name__ == "__main__":
    unittest.main()
