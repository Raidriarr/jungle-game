from jungle_game.model.position import Position
from jungle_game.model.piece import Piece
from jungle_game.model.animal_type import (
    ELEPHANT, LION, TIGER, LEOPARD, WOLF, DOG, CAT, RAT
)
LAND = 0
RIVER = 1
TRAP_P1 = 2
TRAP_P2 = 3
DEN_P1 = 4
DEN_P2 = 5


class Board:
    def __init__(self):
        self.tiles = [
            [LAND, LAND, TRAP_P2, DEN_P2, TRAP_P2, LAND, LAND],
            [LAND, LAND, LAND, TRAP_P2, LAND, LAND, LAND],
            [LAND, LAND, LAND, LAND, LAND, LAND, LAND],
            [LAND, RIVER, RIVER, LAND, RIVER, RIVER, LAND],
            [LAND, RIVER, RIVER, LAND, RIVER, RIVER, LAND],
            [LAND, RIVER, RIVER, LAND, RIVER, RIVER, LAND],
            [LAND, LAND, LAND, LAND, LAND, LAND, LAND],
            [LAND, LAND, LAND, TRAP_P1, LAND, LAND, LAND],
            [LAND, LAND, TRAP_P1, DEN_P1, TRAP_P1, LAND, LAND]
        ]
        self.pieces = [
            [None for _ in range(7)]
            for _ in range(9)
        ]
        self.setup_initial_positions()

    def setup_initial_positions(self):
        # ---- Player 2 (TOP of your board) ----
        self.pieces[0][0] = Piece(LION, -1, Position(0, 0))
        self.pieces[0][6] = Piece(TIGER, -1, Position(0, 6))

        self.pieces[1][1] = Piece(DOG, -1, Position(1, 1))
        self.pieces[1][5] = Piece(CAT, -1, Position(1, 5))

        self.pieces[2][0] = Piece(RAT, -1, Position(2, 0))
        self.pieces[2][2] = Piece(LEOPARD, -1, Position(2, 2))
        self.pieces[2][4] = Piece(WOLF, -1, Position(2, 4))
        self.pieces[2][6] = Piece(ELEPHANT, -1, Position(2, 6))

        # ---- Player 1 (BOTTOM of your board) ----
        self.pieces[8][0] = Piece(TIGER, 1, Position(8, 0))
        self.pieces[8][6] = Piece(LION, 1, Position(8, 6))

        self.pieces[7][1] = Piece(CAT, 1, Position(7, 1))
        self.pieces[7][5] = Piece(DOG, 1, Position(7, 5))

        self.pieces[6][0] = Piece(ELEPHANT, 1, Position(6, 0))
        self.pieces[6][2] = Piece(WOLF, 1, Position(6, 2))
        self.pieces[6][4] = Piece(LEOPARD, 1, Position(6, 4))
        self.pieces[6][6] = Piece(RAT, 1, Position(6, 6))

    def get_piece(self, position):
        return self.pieces[position.row][position.col]

    def is_inside(self, position):
        return 0 <= position.row <= 8 and 0 <= position.col <= 6

    def get_tile_type(self, position):
        return self.tiles[position.row][position.col]

    def is_river(self, position):
        return self.tiles[position.row][position.col] == RIVER

    def is_trap_for_player(self, position, player):
        if player == 1:
            return self.tiles[position.row][position.col] == TRAP_P2
        else:
            return self.tiles[position.row][position.col] == TRAP_P1

    def is_den_for_player(self, position, player):
        if player == 1:
            return self.tiles[position.row][position.col] == DEN_P2
        else:
            return self.tiles[position.row][position.col] == DEN_P1
    def move_piece(self, from_pos, to_pos):
        moving_piece = self.get_piece(from_pos)
        captured_piece = self.get_piece(to_pos)  # could be None
        # remove from old square
        self.pieces[from_pos.row][from_pos.col] = None
        # place piece in new square
        self.pieces[to_pos.row][to_pos.col] = moving_piece
        # update its internal position
        moving_piece.position = to_pos
        # if there was an enemy piece there, you *might* mark it as dead
        if captured_piece is not None:
            captured_piece.alive = False
        return captured_piece

    def is_legal_move(self, piece, target_pos, current_player):
        if piece is None:
            return False

        # must move your own piece
        if piece.player != current_player:
            return False

        start = piece.position

        # target must be on board
        if not self.is_inside(target_pos):
            return False

        # cannot stay in place
        if start.row == target_pos.row and start.col == target_pos.col:
            return False

        dest_tile = self.get_tile_type(target_pos)

        # cannot enter your own den (only opponent's)
        if current_player == 1 and dest_tile == DEN_P1:
            return False
        if current_player == -1 and dest_tile == DEN_P2:
            return False

        # -------- movement shape: 1-step or lion/tiger jump --------
        dr = target_pos.row - start.row
        dc = target_pos.col - start.col
        adr, adc = abs(dr), abs(dc)

        # no diagonal moves
        if adr != 0 and adc != 0:
            return False

        jumping = False

        if adr + adc == 1:
            # normal adjacent step (all pieces can do this)
            pass
        else:
            # must be a lion/tiger river jump
            if not piece.animal_type.can_jump_river():
                return False

            # cannot jump *into* the river
            if dest_tile == RIVER:
                return False

            # all squares in between must be river, and no rat may be there
            step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
            step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

            r, c = start.row + step_r, start.col + step_c
            while r != target_pos.row or c != target_pos.col:
                pos = Position(r, c)
                # every intermediate square must be river
                if not self.is_river(pos):
                    return False
                mid_piece = self.get_piece(pos)
                # jump blocked if any rat (friend or enemy) is in the river
                if mid_piece is not None and mid_piece.animal_type.name == "Rat":
                    return False
                r += step_r
                c += step_c

            jumping = True

        # -------- terrain restriction for destination --------
        # only rats may enter water squares
        if dest_tile == RIVER and not piece.animal_type.can_enter_water():
            return False

        # -------- capture rules --------
        target_piece = self.get_piece(target_pos)
        if target_piece is None:
            # empty square → movement rules already checked, so it's legal
            return True

        # cannot capture your own piece
        if target_piece.player == piece.player:
            return False

        attacker = piece
        defender = target_piece
        attacker_pos = start
        defender_pos = target_pos

        # 1. elephant can NEVER capture rat
        if attacker.animal_type.name == "Elephant" and defender.animal_type.name == "Rat":
            return False

        # 2. rat capturing elephant (not from water)
        if attacker.animal_type.name == "Rat" and defender.animal_type.name == "Elephant":
            if self.is_river(attacker_pos):
                return False
            return True

        # 3. if defender is in attacker's trap, attacker can capture regardless of rank
        if self.is_trap_for_player(defender_pos, defender.player):
            return True

        # rat vs rat water rule:
        if attacker.animal_type.name == "Rat" and defender.animal_type.name == "Rat":
            attacker_in_water = self.is_river(attacker_pos)
            defender_in_water = self.is_river(defender_pos)
            # cannot attack from water to land or land to water
            if attacker_in_water != defender_in_water:
                return False
            # same environment (both land or both water) → allowed (same rank)
            return True

        # general rank rule (no traps): attacker rank must be >= defender rank
        return attacker.animal_type.rank >= defender.animal_type.rank

    def can_jump_river(self, piece, from_pos, to_pos):
        # Only lion or tiger can jump
        if not piece.animal_type.can_jump_river():
            return False

        dr = to_pos.row - from_pos.row
        dc = to_pos.col - from_pos.col

        # Jump must be strictly horizontal or vertical
        if dr != 0 and dc != 0:
            return False

        # Cannot jump zero distance
        if dr == 0 and dc == 0:
            return False

        # Determine step direction
        step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
        step_c = 0 if dc == 0 else (1 if dc > 0 else -1)

        r = from_pos.row + step_r
        c = from_pos.col + step_c

        # Must jump OVER the river:
        while (r != to_pos.row) or (c != to_pos.col):
            intermediate = Position(r, c)

            # If any intermediate square is not river → no jump
            if not self.is_river(intermediate):
                return False

            mid_piece = self.get_piece(intermediate)
            if mid_piece is not None and mid_piece.animal_type.name == "Rat":
                # Rats block jumps
                return False

            r += step_r
            c += step_c

        # Final landing tile must NOT be river
        if self.is_river(to_pos):
            return False

        return True
    
    def get_size(self):
        return len(self.tiles), len(self.tiles[0])