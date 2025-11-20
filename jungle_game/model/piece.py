class Piece:
    def __init__(self, animal_type, player, position):
        self.animal_type = animal_type
        self.player = player
        self.position = position
        self.alive = True

    def can_capture(self, other, board):
        # TODO: later: rank rules, rat vs elephant, traps, water
        pass

    def move_to(self, new_position):
        # TODO: later: update position
        pass

    def is_enemy(self, other):
        # TODO: later: check if self.player != other.player
        pass
