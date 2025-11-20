# Tile type constants
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