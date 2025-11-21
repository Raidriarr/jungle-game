class GameState:
    """
    TEMPORARY dummy implementation so that controller + GUI can work.
    Trofim will later replace the internals but KEEP the same method names.
    """

    def __init__(self) -> None:
        # 9 rows x 7 columns simple board filled with dots
        self.rows = 9
        self.cols = 7
        self.board = [["." for _ in range(self.cols)] for _ in range(self.rows)]

        # Just to show something on screen:
        # place a few fake animals
        self.board[2][3] = "L"   # Lion
        self.board[6][1] = "R"   # Rat
        self.board[0][3] = "D"   # Den (example)

    @classmethod
    def new_game(cls) -> "GameState":
        """Factory method – real model can also use this name."""
        return cls()

    def __str__(self) -> str:
        """
        Simple text representation of the board for now.
        GUI will display this.
        """
        lines = []
        header = "   " + " ".join(str(c) for c in range(self.cols))
        lines.append(header)
        for r in range(self.rows):
            row_str = f"{r}  " + " ".join(self.board[r])
            lines.append(row_str)
        return "\n".join(lines)