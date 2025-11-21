# from jungle_game.model.board import Board
from jungle_game.model.game_state import GameState

class GameController:
    def __init__(self, game_state):
         self.game_state= game_state

    @classmethod
    def new_game(cls):
        gs = GameState.new_game()
        return cls(game_state = gs)
    
    def get_board_text(self) -> str:
        return str(self.game_state)
