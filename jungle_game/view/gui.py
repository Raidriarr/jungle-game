from jungle_game.controller.game_controller import GameController
import tkinter as tk

class JungleGameApp (tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        # Window Settings
        self.title = "Jungle Game"
        self.resizable (False,False)

        self.board_label= tk.Label(self, font=("Consolas", 14), justify='left', anchor='w', fg='black')
        self.board_label.pack(padx=10, pady=10)

        #Creating controller with new Game
        self.controller = GameController.new_game()

        # quit button
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.pack(pady=(0, 10))

        self.refresh_board()
        
    def refresh_board(self)-> None:
        board_text = self.controller.get_board_text()
        self.board_label.config(text= board_text)

def main() -> None:
        app = JungleGameApp()
        app.mainloop()

if __name__ == "__main__":
    main()
