from jungle_game.model.animal_type import RAT, CAT, DOG, WOLF, TIGER, LION, ELEPHANT, LEOPARD

class Piece:
    def __init__(self, animal_type, player, position):
        self.animal_type = animal_type
        self.player = player
        self.position = position
        self.alive = True

    def get_name(self):
        symbol_map = {
            RAT: 'Rat',
            CAT: 'Cat',
            DOG: 'Dog',
            WOLF: 'Wolf',
            LEOPARD: 'Leopard',
            TIGER: 'Tiger',
            LION: 'Lion',
            ELEPHANT: 'Elephant'
        }
        symbol = symbol_map.get(self.animal_type, '?')
        return symbol.lower() if self.player == -1 else symbol.upper()
