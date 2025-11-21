from jungle_game.model.game_state import GameState
from jungle_game.model.position import Position


class GameController:
    def __init__(self, game_state=None):
        # If no game_state passed, create a new one
        self.game_state = game_state or GameState()

    @classmethod
    def new_game(cls):
        return cls(GameState())

    def get_current_player(self):
        return self.game_state.get_current_player()

    def get_board(self):
        return self.game_state.board

    def make_move(self, from_row, from_col, to_row, to_col):
        from_pos = Position(from_row, from_col)
        to_pos = Position(to_row, to_col)
        return self.game_state.make_move(from_pos, to_pos)

    def undo(self):
        """
        Undo the *last actual move* made in the game.
        This is the correct behaviour for Jungle and for your GameState.

        A player should always be able to undo *their own last move*,
        regardless of whose turn it currently is.
        """
        # No moves made → nothing to undo
        if not self.game_state.move_history:
            return False

        # The player who made the last move (stored in history)
        last_player = self.game_state.move_history[-1][3]

        # Check if that player is allowed to undo
        if self.game_state.can_undo(last_player):
            return self.game_state.undo_last_move()

        return False

    def is_game_over(self):
        return self.game_state.is_game_over()

    def get_winner(self):
        return self.game_state.get_winner()
