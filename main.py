import tkinter as tk
from tkinter import messagebox
import minesweeper

import random

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = minesweeper.Minesweeper(root)
    root.mainloop()
