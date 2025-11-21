from .position import Position
from .board import Board, DEN_P1, DEN_P2
import json

class GameState:
    def __init__(self):
        self.board = Board()
        self.current_player = 1   # 1 for Player 1, -1 for Player 2
        self.move_history = []    # list of moves (from, to, captured piece, etc.)
        self.undo_used = {1: 0, -1: 0}   # how many undos each player used
        self.game_over = False
        self.winner = None        # 1, -1, or None

    def make_move(self, from_pos, to_pos):
        if self.game_over:
            return False
        piece = self.board.get_piece(from_pos)
        if piece is None:
            return False
        if piece.player != self.current_player:
            return False
        if not self.board.is_legal_move(piece, to_pos, self.current_player):
            return False
        captured_piece = self.board.get_piece(to_pos)
        self.board.move_piece(from_pos, to_pos)
        piece.position = to_pos
        self.move_history.append((from_pos, to_pos, captured_piece, self.current_player))
        dest_tile = self.board.get_tile_type(to_pos)
        if self.current_player == 1 and dest_tile == DEN_P2:
            self.game_over = True
            self.winner = 1
            return True
        if self.current_player == -1 and dest_tile == DEN_P1:
            self.game_over = True
            self.winner = -1
            return True
        opponent = -self.current_player
        opponent_has_piece = False
        for row in range(9):
            for col in range(7):
                p = self.board.pieces[row][col]
                if p is not None and p.player == opponent:
                    opponent_has_piece = True
                    break
            if opponent_has_piece:
                break
        if not opponent_has_piece:
            self.game_over = True
            self.winner = self.current_player
            return True
        self.switch_player()
        return True

    def switch_player(self):
        self.current_player *= -1

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner

    def can_undo(self, player):
        if self.game_over:
            return False

        if not self.move_history:
            return False

            # Check who made the last move
        _, _, _, last_move_player = self.move_history[-1]

        if last_move_player != player:
            return False

        if self.undo_used[player] >= 3:
            return False

        return True

    def undo_last_move(self):
        if not self.move_history:
            return False  # nothing to undo

            # Extract last recorded move
        from_pos, to_pos, captured_piece, player = self.move_history.pop()

        # We will undo the move made by 'player'
        moved_piece = self.board.get_piece(to_pos)

        if moved_piece is None:
            # Should never happen if code is correct
            return False

        # 1. Move the piece back to original square
        self.board.pieces[to_pos.row][to_pos.col] = None
        self.board.pieces[from_pos.row][from_pos.col] = moved_piece
        moved_piece.position = from_pos

        # 2. Restore captured piece (if any)
        if captured_piece is not None:
            self.board.pieces[to_pos.row][to_pos.col] = captured_piece
            captured_piece.alive = True
            captured_piece.position = to_pos

        # 3. Switch current player BACK to the one who made the undone move
        self.current_player = player

        # 4. Mark undo used
        self.undo_used[player] += 1

        # 5. If the game was previously over, undo resets it
        self.game_over = False
        self.winner = None

        return True

    def get_legal_moves(self, player):
        moves = []

        # Directions for orthogonal movement
        DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for row in range(9):
            for col in range(7):
                piece = self.board.pieces[row][col]

                if piece is None:
                    continue
                if piece.player != player:
                    continue

                from_pos = piece.position

                # try all 4 directions
                for dr, dc in DIRECTIONS:
                    to_row = row + dr
                    to_col = col + dc
                    target_pos = Position(to_row, to_col)

                    if not self.board.is_inside(target_pos):
                        continue

                    if self.board.is_legal_move(piece, target_pos, player):
                        moves.append((from_pos, target_pos))

                # also try possible jump directions (lion/tiger)
                # Jumps are far, but is_legal_move handles legality.
                # So test squares in same row/col.
                if piece.animal_type.can_jump_river():
                    # same row, different columns
                    for col2 in range(7):
                        if col2 == col:
                            continue
                        target_pos = Position(row, col2)
                        if self.board.is_legal_move(piece, target_pos, player):
                            moves.append((from_pos, target_pos))

                    # same column, different rows
                    for row2 in range(9):
                        if row2 == row:
                            continue
                        target_pos = Position(row2, col)
                        if self.board.is_legal_move(piece, target_pos, player):
                            moves.append((from_pos, target_pos))
        return moves
    
    def get_current_player(self):
        return self.current_player

    #Save into .jungle format
    def save_game(self, filename):
        data = self.to_dict()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    #Save into .record format
    def save_record(self, filename):
        with open(filename, "w") as f:
            for fr, to, cap, pl in self.move_history:
                r1, c1 = fr.get_pos()
                r2, c2 = to.get_pos()
                f.write(f"{r1} {c1} {r2} {c2}\n")

    def to_dict(self):
        pieces_data = []

        for row in range(9):
            row_data = []
            for col in range(7):
                piece = self.board.pieces[row][col]
                if piece is None:
                    row_data.append(None)
                else:
                    row_data.append({
                        "type": piece.animal_type.name,
                        "player": piece.player
                    })
            pieces_data.append(row_data)

        return {
            "current_player": self.current_player,
            "undo_used": {
                "1": self.undo_used[1],
                "-1": self.undo_used[-1]
            },
            "pieces": pieces_data
        }

    # Load from .jungle format
    @classmethod
    def load_game(cls, filename):
        state = cls()  # create a fresh game

        with open(filename, 'r') as f:
            data = json.load(f)

        state.current_player = data["current_player"]
        state.undo_used = {
            1: data["undo_used"]["1"],
            -1: data["undo_used"]["-1"]
        }

        # rebuild board pieces
        pieces_data = data["pieces"]

        for row in range(9):
            for col in range(7):
                entry = pieces_data[row][col]

                if entry is None:
                    state.board.pieces[row][col] = None
                    continue

                # recreate the piece
                piece_type = entry["type"]
                player = entry["player"]

                # find correct AnimalType instance
                from .animal_type import (
                    ELEPHANT, LION, TIGER, LEOPARD,
                    WOLF, DOG, CAT, RAT
                )
                type_map = {
                    "Elephant": ELEPHANT,
                    "Lion": LION,
                    "Tiger": TIGER,
                    "Leopard": LEOPARD,
                    "Wolf": WOLF,
                    "Dog": DOG,
                    "Cat": CAT,
                    "Rat": RAT
                }

                animal_type = type_map[piece_type]

                from .position import Position
                from .piece import Piece

                pos = Position(row, col)
                piece_obj = Piece(animal_type, player, pos)

                state.board.pieces[row][col] = piece_obj

        return state
    
    @classmethod
    def replay_history(cls, filename):  
        moves = []
        with open(filename, "r") as f:
            for line in f:
                r1, c1, r2, c2 = map(int, line.strip().split())
                moves.append((r1, c1, r2, c2))
        return moves
        
        
        





