import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, master, rows=10, columns=10, mines=10):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.buttons = []
        self.flags = 0
        self.mine_positions = set()
        self.game_over = False

        self.frame = tk.Frame(master)
        self.frame.pack()

        self.create_widgets()
        self.place_mines()
        self.update_numbers()

    def create_widgets(self):
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                button = tk.Button(self.frame, text="", width=3, command=lambda r=r, c=c: self.click(r, c))
                button.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))
                button.grid(row=r, column=c)
                row.append(button)
            self.buttons.append(row)

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.columns - 1)
            self.mine_positions.add((r, c))

    def update_numbers(self):
        self.numbers = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        for r, c in self.mine_positions:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns and (nr, nc) not in self.mine_positions:
                        self.numbers[nr][nc] += 1

    def click(self, r, c):
        if self.game_over:
            return
        if (r, c) in self.mine_positions:
            self.buttons[r][c].config(text="*", bg="red")
            self.game_over = True
            self.reveal_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
        else:
            self.reveal(r, c)
            self.check_win()

    def right_click(self, r, c):
        if self.game_over:
            return
        if self.buttons[r][c]["text"] == "F":
            self.buttons[r][c]["text"] = ""
            self.flags -= 1
        else:
            self.buttons[r][c]["text"] = "F"
            self.flags += 1
        self.check_win()

    def reveal(self, r, c):
        if self.buttons[r][c]["state"] == "disabled":
            return
        self.buttons[r][c]["text"] = self.numbers[r][c]
        self.buttons[r][c]["state"] = "disabled"
        self.buttons[r][c].config(relief=tk.SUNKEN, bg="lightgrey")
        if self.numbers[r][c] == 0:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.columns:
                        self.reveal(nr, nc)

    def reveal_mines(self):
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text="*", bg="red")

    def check_win(self):
        win = True
        for r in range(self.rows):
            for c in range(self.columns):
                if self.buttons[r][c]["state"] != "disabled" and (r, c) not in self.mine_positions:
                    win = False
                if self.buttons[r][c]["text"] == "F" and (r, c) not in self.mine_positions:
                    win = False
        if win:
            self.game_over = True
            messagebox.showinfo("Congratulations", "You won!")

