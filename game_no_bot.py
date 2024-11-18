import tkinter as tk
import math
import random
import time

class RouletteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Roulette Game")
        self.root.geometry("700x700")
        self.root.resizable(False, False)

        self.numbers = [
            (0, "green"), (32, "red"), (15, "black"), (19, "red"), (4, "black"),
            (21, "red"), (2, "black"), (25, "red"), (17, "black"), (34, "red"),
            (6, "black"), (27, "red"), (13, "black"), (36, "red"), (11, "black"),
            (30, "red"), (8, "black"), (23, "red"), (10, "black"), (5, "red"),
            (24, "black"), (16, "red"), (33, "black"), (1, "red"), (20, "black"),
            (14, "red"), (31, "black"), (9, "red"), (22, "black"), (18, "red"),
            (29, "black"), (7, "red"), (28, "black"), (12, "red"), (35, "black"),
            (3, "red"), (26, "black")
        ]

        self.balance = 1000
        self.bet_amount = 50
        self.selected_color = None
        self.result_number = None
        self.rotation_angle = 0

        self.create_widgets()

    def create_widgets(self):
        self.balance_label = tk.Label(self.root, text=f"Balance: ₹{self.balance}", font=("Arial", 16))
        self.balance_label.pack(pady=10)

        self.bet_label = tk.Label(self.root, text="Enter Bet Amount:", font=("Arial", 12))
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root, font=("Arial", 12), justify="center")
        self.bet_entry.pack(pady=5)

        self.color_label = tk.Label(self.root, text="Choose Color (Red/Black):", font=("Arial", 12))
        self.color_label.pack()
        self.color_var = tk.StringVar(value="red")
        tk.Radiobutton(self.root, text="Red", variable=self.color_var, value="red", font=("Arial", 12)).pack()
        tk.Radiobutton(self.root, text="Black", variable=self.color_var, value="black", font=("Arial", 12)).pack()

        self.spin_button = tk.Button(self.root, text="Spin", font=("Arial", 14), command=self.spin_wheel)
        self.spin_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
        self.canvas.pack()
        self.draw_wheel()

        self.pointer = self.canvas.create_polygon(250, 50, 230, 70, 270, 70, fill="black")

    def draw_wheel(self):
        cx, cy = 250, 250
        radius = 200
        num_segments = len(self.numbers)

        self.canvas.delete("wheel")

        for i, (number, color) in enumerate(self.numbers):
            start_angle = (i * (360 / num_segments)) + self.rotation_angle
            extent_angle = 360 / num_segments

            self.canvas.create_arc(
                cx - radius, cy - radius, cx + radius, cy + radius,
                start=start_angle, extent=extent_angle,
                fill=color, outline="black", tags="wheel"
            )

            angle_rad = math.radians(start_angle + extent_angle / 2)
            x = cx + (radius - 30) * math.cos(angle_rad)
            y = cy - (radius - 30) * math.sin(angle_rad)
            self.canvas.create_text(x, y, text=str(number), font=("Arial", 10), fill="white", tags="wheel")

    def spin_wheel(self):
        try:
            self.bet_amount = int(self.bet_entry.get())
            if self.bet_amount <= 0 or self.bet_amount > self.balance:
                raise ValueError("Invalid bet amount.")
        except ValueError:
            self.result_label.config(text="Enter a valid bet amount!", fg="red")
            return

        self.selected_color = self.color_var.get()
        self.result_label.config(text="Spinning...", fg="blue")
        self.root.update()

        spins = 3
        num_segments = len(self.numbers)
        start_index = random.randint(0, num_segments - 1)

        for i in range(360 * spins):
            self.rotation_angle = (self.rotation_angle + 3) % 360
            self.draw_wheel()
            self.canvas.update()
            time.sleep(0.005)

        result_index = (start_index + self.rotation_angle // (360 // num_segments)) % num_segments
        self.result_number, result_color = self.numbers[result_index]

        self.result_label.config(
            text=f"You Won! Number: {self.result_number} ({result_color.capitalize()})" if self.selected_color == result_color else f"You Lost! Number: {self.result_number} ({result_color.capitalize()})",
            fg="green" if self.selected_color == result_color else "red"
        )

        if self.selected_color == result_color:
            self.balance += self.bet_amount
        else:
            self.balance -= self.bet_amount

        self.balance_label.config(text=f"Balance: ₹{self.balance}")
        self.log_bet(self.bet_amount, self.result_number, result_color)

    def log_bet(self, bet_amount, result_number, result_color):
        with open("roulette_bets.txt", "a") as file:
            file.write(f"Bet: ₹{bet_amount}, Result: {result_number} ({result_color.capitalize()}), Balance: ₹{self.balance}\n")

if __name__ == "__main__":
    root = tk.Tk()
    game = RouletteGame(root)
    root.mainloop()

