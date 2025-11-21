from jungle_game.model.game_state import GameState
from jungle_game.model.position import Position


class GameController:
    def __init__(self, game_state=None):
        self.game_state = game_state or GameState()

    @classmethod
    def new_game(cls):
        return cls(GameState())
    
    #Get Board Info
    def get_current_player(self):
        return self.game_state.get_current_player()
    
    def get_board_size(self):
        return self.game_state.board.get_size()
    
    def get_tile_type(self, row, col):
        position = Position(row, col)
        t= self.game_state.board.get_tile_type(position)
        type_map = {
            0: "land",
            1: "river",
            2: "trap1",
            3: "trap2",
            4: "den1",
            5: "den2"
        }
        return type_map.get(t, "UNKNOWN")
    
    def get_piece_at(self, row, col):
        position = Position(row, col)
        return self.game_state.board.get_piece(position)
    
    def get_piece_name(self, row, col):
        piece = self.get_piece_at(row, col)
        if piece is None:
            return None
        return piece.get_name()

    #Actions
    def can_select_piece(self, row, col):
        position = Position(row, col)
        piece = self.game_state.board.get_piece(position)
        if piece is None:
            return False
        return piece.player == self.game_state.current_player

    def make_move(self, from_row, from_col, to_row, to_col):
        from_pos = Position(from_row, from_col)
        to_pos = Position(to_row, to_col)
        return self.game_state.make_move(from_pos, to_pos)

    def undo(self):
        if self.game_state.can_undo(self.game_state.current_player):
            return self.game_state.undo_last_move()
        return False

    #Game State Info
    def is_game_over(self):
        return self.game_state.is_game_over()

    def get_winner(self):
        return self.game_state.get_winner()
