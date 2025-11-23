# main.py  (put this in the project root, next to jungle_game/)

from jungle_game.view.gui import JungleGameApp


def main():
    print("====================================")
    print("   Welcome to the Jungle Game! 🐯")
    print("====================================")
    print()

    while True:
        answer = input("Do you want to start a new game? (y/n): ").strip().lower()

        if answer in ("y", "yes"):
            print("Starting GUI... (close the window to exit the game)")
            app = JungleGameApp()
            app.mainloop()
            print("Thanks for playing!")
            break

        elif answer in ("n", "no"):
            print("Okay, maybe next time. Goodbye!")
            break

        else:
            print("Please type 'y' or 'n' and press Enter.")


if __name__ == "__main__":
    main()
