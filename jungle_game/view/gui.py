from jungle_game.controller.game_controller import GameController
import tkinter as tk
from tkinter import filedialog


class JungleGameApp (tk.Tk):
    #GUI itself
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
        # Frame that holds row labels (left) + board itself
        self.main_board_frame = tk.Frame(self)
        self.main_board_frame.pack(padx=10, pady=10)

        # Frame for row numbers on the left
        self.row_label_frame = tk.Frame(self.main_board_frame)
        self.row_label_frame.grid(row=0, column=0, padx=(0, 5))
        
        # Board Frame (actual grid of pieces)
        self.board_frame = tk.Frame(self.main_board_frame)
        self.board_frame.grid(row=0, column=1)

        rows, cols = self.controller.get_board_size()
        self.rows = rows
        self.cols = cols

        #Board colors
        self.cell_labels: list[list[tk.Label]] = []
        self.base_bg: list[list[str]] = []  # store base background color per cell

        # Create row labels: 9 at top → 1 at bottom
        for r in range(rows):
            num = str(rows - r)   # row 0 -> "9", row 8 -> "1"
            tk.Label(self.row_label_frame, text=num, font=("Consolas", 16), height=2, anchor="center").grid(
                row=r, column=0, pady=1
            )

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

        # Bottom column labels (A–G)
        self.col_label_frame = tk.Frame(self)
        self.col_label_frame.pack(padx=10, pady=(0, 10))

        # Small spacer under the row-number column
        tk.Label(self.col_label_frame, text=" ", font=("Consolas", 14), width=5, height=0).grid(row=0, column=0)

        for c in range(cols):
            letter = chr(ord("A") + c)
            tk.Label(self.col_label_frame, text=letter, font=("Consolas", 15), width=5, anchor='w').grid(
                row=0, column=c + 1, padx=1
            )

        # Control buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=(0, 30))

        new_button = tk.Button(buttons_frame, text="New Game", command=self.reset_game)
        new_button.grid(row=0, column=0, padx=5)
        
        save_button = tk.Button(buttons_frame, text="Save", command=self.save_game)
        save_button.grid(row=0, column=1, padx=5)
        
        load_button = tk.Button(buttons_frame, text="Load", command=self.load_game)
        load_button.grid(row=0, column=2, padx=5)

        replay_button = tk.Button(buttons_frame, text="Replay", command=self.replay_moves)
        replay_button.grid(row=0, column=3, padx=5)

        undo_button = tk.Button(buttons_frame, text="Undo", command=self.on_undo)
        undo_button.grid(row=0, column=4, padx=5)

        quit_button = tk.Button(buttons_frame, text="Quit", command=self.destroy)
        quit_button.grid(row=0, column=5, padx=5)

        #First board refresh to Initialize display
        self.refresh_board()

###################################################################################
    #Events Handler
    def on_cell_click(self, row, col):
        if self.controller.is_game_over():
            return
        if self.selected_cell is None:
            if self.controller.can_select_piece(row, col):
                self.selected_cell = (row, col)

                # Need to highlight selected cell and possible moves for it
                self.cell_labels[row][col].config(bg="#ffff99")  # Highlight selected cell
                piece_name = self.controller.get_piece_name(row, col)
                self.status_label.config(text=f"Selected {piece_name.capitalize()}")
            else:
                self.status_label.config(text="Cannot select this piece.")
                self.after(2000, self.restore_player_turn)
        else:
            from_row, from_col = self.selected_cell
            # Unselect
            if from_row == row and from_col == col:
                self.selected_cell = None
                self.refresh_board()
            
            if self.controller.make_move(from_row, from_col, row, col):
                self.selected_cell=None
                self.status_label.config(text=f"Moved piece.")
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

    def reset_game(self):
        self.controller = GameController.new_game()
        self.selected_cell = None
        self.refresh_board()
        self.status_label.config(text="New game started. Player 1's turn.")

    def save_game(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".jungle",
            filetypes=[("Jungle Game Files", "*.jungle"), ("Records", "*.record")],
        )
        if not filename:
            return 
        
        self.controller.save_game(filename)
        self.status_label.config(text=f"Game saved to {filename}")
        self.after(2000, self.restore_player_turn)

    def open_file_dialog(self, type):
        filename = filedialog.askopenfilename(
            title="Open Jungle Game File",
            filetypes=[type ]
        )
        return filename

    def load_game(self, type=("Jungle Game Files", "*.jungle")):
        filename = self.open_file_dialog(type)
        if not filename:
            self.status_label.config(text=f"Failed to load, Try again.")
            self.after(2000, self.restore_player_turn)
            return
            
        self.controller.load_game(filename)
        self.selected_cell = None
        self.refresh_board()
        self.status_label.config(text=f"Loaded game from {filename}")
        self.after(2000, self.restore_player_turn)
    
    def replay_moves(self, type=("Records", "*.record")):
        filename = self.open_file_dialog(type)
        if not filename:
            self.status_label.config(text=f"Failed to load, Try again.")
            self.after(2000, self.restore_player_turn)
            return
            
        self.status_label.config(text=f"Replaing from {filename}")

        moves= self.controller.replay_game(filename)
        self.refresh_board()
        self.after(1000, lambda: self.animate_replay(0, moves))
        self.refresh_board()

    def animate_replay(self, index, moves):
        if index >= len(moves):
            self.status_label.config(text="Replay finished.")
            self.refresh_board()
            return
        move = moves[index]
        self.controller.apply_move_tuple(move)
        self.refresh_board()

        self.after(1000, lambda: self.animate_replay(index + 1, moves))
        

######################################
    #Refreshing Board Display/GUI
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
            self.restore_player_turn()
            return

        self.status_label.config(text=text)

    def restore_player_turn(self):
        player = self.controller.get_current_player()
        self.status_label.config(text=f"Player {1 if player == 1 else 2}'s turn")
        return


def main() -> None:
        app = JungleGameApp()
        app.mainloop()

if __name__ == "__main__":
    main()
