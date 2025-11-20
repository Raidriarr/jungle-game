class AnimalType:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank

    def can_enter_water(self):
        return self.name == "Rat"

    def can_jump_river(self):
        return self.name == "Lion" or self.name == "Tiger"


ELEPHANT = AnimalType("Elephant", 8)
LION = AnimalType("Lion", 7)
TIGER = AnimalType("Tiger", 6)
LEOPARD = AnimalType("Leopard", 5)
WOLF = AnimalType("Wolf", 4)
DOG = AnimalType("Dog", 3)
CAT = AnimalType("Cat", 2)
RAT = AnimalType("Rat", 1)
