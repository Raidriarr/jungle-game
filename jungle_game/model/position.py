class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def is_adjacent(self, other):
        r = abs(self.row - other.row)
        c = abs(self.col - other.col)
        return r + c == 1
    
    def get_pos(self):
        return self.row, self.col
