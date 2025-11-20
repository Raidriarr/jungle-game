class GameState:
    def __init__(self):
        """
        Create a new game:
        - set up the board
        - set starting player
        - prepare move history and undo limits
        - mark game as not over
        """
        # self.board = Board()
        # self.current_player = 1   # 1 for Player 1, -1 for Player 2
        # self.move_history = []    # list of moves (from, to, captured piece, etc.)
        # self.undo_used = {1: 0, -1: 0}   # how many undos each player used
        # self.game_over = False
        # self.winner = None        # 1, -1, or None
        pass

    def make_move(self, from_pos, to_pos):
        """
        Try to make a move for current_player from from_pos to to_pos.

        Steps (later in logic):
        - get the piece at from_pos from the board
        - ask board.is_legal_move(piece, to_pos, current_player)
        - if not legal: return False (or raise)
        - if legal:
            - call board.move_piece(from_pos, to_pos) and get captured_piece
            - store a record in self.move_history (from, to, captured_piece, maybe previous den/trap info)
            - check if the move ends the game (entering den or capturing last piece)
            - if game ended: set self.game_over and self.winner
            - else: switch player
        """
        pass

    def switch_player(self):
        """
        Switch current_player between 1 and -1.
        Example: self.current_player = -self.current_player
        """
        pass

    def is_game_over(self):
        """
        Return True if the game has ended.
        You can either:
        - just return self.game_over, or
        - recompute (e.g. check if a den is occupied or a player has no pieces left).
        """
        pass

    def get_winner(self):
        """
        Return the winner:
        - 1  if Player 1 wins
        - -1 if Player 2 wins
        - None if there is no winner yet or it's a draw (if you allow draws).
        """
        pass

    def can_undo(self, player):
        """
        Return True if the given player is allowed to undo a move.
        Typical rules:
        - each player has at most 3 undos
        - cannot undo if there is no history
        - maybe only undo your own last move (depends on assignment spec)
        """
        pass

    def undo_last_move(self):
        """
        Undo the last move.

        Steps (later in logic):
        - check if move_history is not empty
        - pop the last move record (from_pos, to_pos, captured_piece, player, etc.)
        - move the piece back from to_pos to from_pos on the board
        - if captured_piece is not None:
            - put the captured piece back on the board
            - mark captured_piece.alive = True (if you use that flag)
        - update self.current_player back to the player who made that move
        - increase undo_used for that player
        """
        pass

    def get_legal_moves(self, player):
        """
        Return a list of all legal moves for the given player.

        Typical shape of a move: (from_pos, to_pos)

        Steps (later in logic):
        - loop over all board squares
        - find pieces that belong to 'player'
        - for each piece, try all 4 directions (and maybe jumps)
        - call board.is_legal_move(piece, target_pos, player)
        - if True, add to the list
        """
        pass

    def get_current_player(self):
        """
        Return the player whose turn it is (1 or -1).
        """
        pass








