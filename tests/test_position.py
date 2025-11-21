import unittest

from jungle_game.model.position import Position


class TestPosition(unittest.TestCase):
    def test_adjacent_horizontal(self):
        p1 = Position(3, 3)
        p2 = Position(3, 4)
        self.assertTrue(p1.is_adjacent(p2))

    def test_adjacent_vertical(self):
        p1 = Position(3, 3)
        p2 = Position(2, 3)
        self.assertTrue(p1.is_adjacent(p2))

    def test_not_adjacent_diagonal(self):
        p1 = Position(3, 3)
        p2 = Position(4, 4)
        self.assertFalse(p1.is_adjacent(p2))

    def test_not_adjacent_far(self):
        p1 = Position(0, 0)
        p2 = Position(2, 0)
        self.assertFalse(p1.is_adjacent(p2))


if __name__ == "__main__":
    unittest.main()
