from jungle_game.controller.game_controller import GameController
import tkinter as tk

class JungleGameApp (tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Window Settings
        self.title("Jungle Game")
        self.resizable (False,False)

        #Creating controller with new Game
        self.controller = GameController.new_game()

        #Emoji Map
        self.emoji_map = {
            "RAT": "🐭",   # Rat
            "CAT": "🐱",   # Cat
            "DOG": "🐶",   # Dog
            "WOLF": "🐺",   # Wolf
            "LEOPARD": "🐆",   # Leopard
            "TIGER": "🐯",   # Tiger
            "LION": "🦁",   # Lion
            "ELEPHANT": "🐘",   # Elephant
        }

        #Selection
        self.selected_cell = None

        #Status Label
        self.status_label = tk.Label(self, text="", font=("Consolas", 12))
        self.status_label.pack(pady=(5, 0))

        #Board Frame
        self.board_frame = tk.Frame(self)
        self.board_frame.pack(padx=10, pady=10)

        rows, cols = self.controller.get_board_size()
        self.rows = rows
        self.cols = cols

        #Board display
        self.cell_labels: list[list[tk.Label]] = []
        self.base_bg: list[list[str]] = []  # store base background color per cell

        # Creating button cells
        for r in range(rows):
            row_labels: list[tk.Label] = []
            row_bg: list[str] = []
            for c in range(cols):
                tile = self.controller.get_tile_type(r, c)
                if tile == "river":
                    bg = "#9ec5ff"
                elif tile in ("trap1", "trap2"):
                    bg = "#ffd27f"
                elif tile in ("den1", "den2"):
                    bg = "#ff6b6b"
                else:
                    bg = "#f0d9b5"  # land

                lbl = tk.Label(
                    self.board_frame,
                    width=5,
                    height=2,
                    font=("Segoe UI Emoji", 14),
                    borderwidth=1,
                    relief="solid",
                    bg=bg,
                    anchor="center"
                )
                lbl.grid(row=r, column=c, padx=1, pady=1)

                # Bind click
                lbl.bind(
                    "<Button-1>",
                    lambda e, row=r, col=c: self.on_cell_click(row, col)
                )

                row_labels.append(lbl)
                row_bg.append(bg)

            self.cell_labels.append(row_labels)
            self.base_bg.append(row_bg)

        # Control buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=(0, 10))

        undo_button = tk.Button(buttons_frame, text="Undo", command=self.on_undo)
        undo_button.grid(row=0, column=0, padx=5)

        quit_button = tk.Button(buttons_frame, text="Quit", command=self.destroy)
        quit_button.grid(row=0, column=1, padx=5)

        #First board refresh to Initialize display
        self.refresh_board()

    #Event Handler
    def on_cell_click(self, row, col):
        if self.controller.is_game_over():
            return
        if self.selected_cell is None:
            if self.controller.can_select_piece(row, col):
                self.selected_cell = (row, col)

                # Need to highlight selected cell and possible moves for it
                self.cell_labels[row][col].config(bg="#ffff99")  # Highlight selected cell
                piece_name = self.controller.get_piece_name(row, col)
                self.status_label.config(text=f"Selected {piece_name.capitalize()} at ({row}, {col})")
            else:
                self.status_label.config(text="Cannot select this piece.")
        else:
            from_row, from_col = self.selected_cell
            # Unselect
            if from_row == row and from_col == col:
                self.selected_cell = None
                self.refresh_board()
            
            if self.controller.make_move(from_row, from_col, row, col):
                self.selected_cell=None
                self.status_label.config(text=f"Moved piece to ({row}, {col})")
                self.refresh_board()
            else:
                self.status_label.config(text="Illegal move.")
                self.selected_cell = None
                self.refresh_board()

            # Reset all cell backgrounds to base colors
            for r in range(self.rows):
                for c in range(self.cols):
                    self.cell_labels[r][c].config(bg=self.base_bg[r][c])
            self.refresh_board()

    def on_undo(self):
        if self.controller.undo():
            self.selected_cell = None
            self.refresh_board()

    #Refresh Board Display
    def refresh_board(self)-> None:
        rows, cols = self.rows, self.cols
        for r in range(rows):
            for c in range(cols):
                symbol = self.controller.get_piece_name(r, c)
                if symbol==None:
                    emoji = ""
                else:
                    base = symbol.upper()
                    animal = self.emoji_map.get(base, "?")
                    if symbol.isupper():
                        emoji = animal + "⬆️"
                    else:
                        emoji = animal + "⬇️"

                # base background color from tile
                bg = self.base_bg[r][c]

                # highlight selected cell
                if self.selected_cell == (r, c):
                    bg = "#ffff88"  # light yellow

                self.cell_labels[r][c].config(text=emoji, bg=bg)

        # update status text
        if self.controller.is_game_over():
            winner = self.controller.get_winner()
            if winner == 1:
                text = "Game over: Player 1 wins!"
            elif winner == -1:
                text = "Game over: Player 2 wins!"
            else:
                text = "Game over"
        else:
            player = self.controller.get_current_player()
            text = f"Player {1 if player == 1 else 2}'s turn"

        self.status_label.config(text=text)


def main() -> None:
        app = JungleGameApp()
        app.mainloop()

if __name__ == "__main__":
    main()
