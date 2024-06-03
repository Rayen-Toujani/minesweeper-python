import tkinter as tk
import minesweeper



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = minesweeper.Minesweeper(root)
    root.mainloop()
