import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import json
import pygame

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.rows = 10
        self.columns = 10
        self.mines = 10
        self.buttons = []
        self.flags = 0
        self.mine_positions = set()
        self.game_over = False

        # Timer variables
        self.timer_label = None
        self.elapsed_time = 0
        self.timer_running = False

        # Load and resize images
        self.mine_img = Image.open("mine.png").resize((24, 24), Image.LANCZOS)
        self.mine_img = ImageTk.PhotoImage(self.mine_img)
        self.flag_img = Image.open("flag.png").resize((24, 24), Image.LANCZOS)
        self.flag_img = ImageTk.PhotoImage(self.flag_img)

        self.frame = tk.Frame(master)
        self.frame.pack()

        pygame.mixer.init()

        self.mine_sound = pygame.mixer.Sound("BombSoundEffect.m4a")

        self.create_size_buttons()
        self.create_difficulty_buttons()
        self.create_reset_button()
        self.create_high_scores_button()

    def create_size_buttons(self):
        size_frame = tk.Frame(self.master)
        size_frame.pack()

        button10 = tk.Button(size_frame, text="10x10", command=lambda: self.set_size(10, 10, 10))
        button15 = tk.Button(size_frame, text="15x15", command=lambda: self.set_size(15, 15, 30))
        button20 = tk.Button(size_frame, text="20x20", command=lambda: self.set_size(20, 20, 50))

        button10.pack(side=tk.LEFT, padx=10, pady=10)
        button15.pack(side=tk.LEFT, padx=10, pady=10)
        button20.pack(side=tk.LEFT, padx=10, pady=10)

        self.timer_label = tk.Label(self.master, text="Time: 0s")
        self.timer_label.pack(pady=10)

    def create_difficulty_buttons(self):
        difficulty_frame = tk.Frame(self.master)
        difficulty_frame.pack()

        easy_button = tk.Button(difficulty_frame, text="Easy", command=lambda: self.set_size(9, 9, 10))
        medium_button = tk.Button(difficulty_frame, text="Medium", command=lambda: self.set_size(16, 16, 40))
        hard_button = tk.Button(difficulty_frame, text="Hard", command=lambda: self.set_size(30, 16, 99))

        easy_button.pack(side=tk.LEFT, padx=10, pady=10)
        medium_button.pack(side=tk.LEFT, padx=10, pady=10)
        hard_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_reset_button(self):
        reset_button = tk.Button(self.master, text="Reset", command=self.reset_game)
        reset_button.pack(pady=10)

    def create_high_scores_button(self):
        high_scores_button = tk.Button(self.master, text="High Scores", command=self.display_high_scores)
        high_scores_button.pack(pady=10)

    def reset_game(self):
        self.set_size(self.rows, self.columns, self.mines)

    def set_size(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines

        self.buttons = []
        self.flags = 0
        self.mine_positions = set()
        self.game_over = False

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.place_mines()
        self.update_numbers()
        self.reset_timer()

    def create_widgets(self):
        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                button = tk.Button(self.frame, text="", width=3, height=1, command=lambda r=r, c=c: self.click(r, c))
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
        if not self.timer_running:
            self.start_timer()
        if self.game_over:
            return
        if (r, c) in self.mine_positions:
            self.buttons[r][c].config(image=self.mine_img)
            self.game_over = True
            self.mine_sound.play()
            self.reveal_mines()
            self.stop_timer()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
        else:
            self.reveal(r, c)
            self.check_win()

    def right_click(self, r, c):
        if self.game_over:
            return
        if self.buttons[r][c]["text"] == "F":
            self.buttons[r][c]["text"] = ""
            self.buttons[r][c].config(image="")
            self.flags -= 1
        else:
            self.buttons[r][c]["text"] = "F"
            self.buttons[r][c].config(image=self.flag_img)
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
            self.buttons[r][c].config(image=self.mine_img)

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
            self.stop_timer()
            self.save_high_score(self.elapsed_time, f"{self.rows}x{self.columns}")
            messagebox.showinfo("Congratulations", "You won!")

    def reset_timer(self):
        self.elapsed_time = 0
        self.timer_running = False
        self.update_timer()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time += 1
            self.timer_label.config(text=f"Time: {self.elapsed_time}s")
            self.master.after(1000, self.update_timer)

    def save_high_score(self, time, difficulty):
        high_scores = self.load_high_scores()
        if difficulty not in high_scores or time < high_scores[difficulty]:
            high_scores[difficulty] = time
            with open("high_scores.json", "w") as f:
                json.dump(high_scores, f)

    def load_high_scores(self):
        try:
            with open("high_scores.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def display_high_scores(self):
        high_scores = self.load_high_scores()
        message = ""
        for difficulty, score in high_scores.items():
            message += f"{difficulty}: {score}s\n"
        messagebox.showinfo("High Scores", message)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
