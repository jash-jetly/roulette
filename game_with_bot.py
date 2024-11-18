import math
import tkinter as tk
import random
import time

class roulette:
    def __init__(self, root):
        self.root = root
        self.root.title("Roulette")
        self.root.geometry("700x800")
        self.root.resizable=(False, False)

        self.numbers=[
            (0, "green"), (32, "red"), (15, "black"), (19, "red"), (4, "black"),
            (21, "red"), (2, "black"), (25, "red"), (17, "black"), (34, "red"),
            (6, "black"), (27, "red"), (13, "black"), (36, "red"), (11, "black"),
            (30, "red"), (8, "black"), (23, "red"), (10, "black"), (5, "red"),
            (24, "black"), (16, "red"), (33, "black"), (1, "red"), (20, "black"),
            (14, "red"), (31, "black"), (9, "red"), (22, "black"), (18, "red"),
            (29, "black"), (7, "red"), (28, "black"), (12, "red"), (35, "black"),
            (3, "red"), (26, "black")
        ]

        self.balance=1000
        self.bet_amount=1
        self.selected_color="red"
        self.loss_streak=0
        self.max_loss_streak=12
        self.rotation_angle=0

        self.widgets()
        self.auto_bet()

    def widgets(self):

        self.balance_label = tk.Label(self.root, text="Balance: $1000", font=("Arial", 20))
        self.balance_label.pack()

        self.bet_label=tk.Label(self.root, text=f"Betting on Red, amonunt: {self.bet_amount}", font=("Arial", 20))
        self.bet_label.pack()

        self.spin_button = tk.Button(self.root, text="Spin", font=("Arial", 20), state="disabled")
        self.spin_button.pack(pady=10)

        self.result_label=tk.Label(self.root, text="", font=("Arial", 20))
        self.result_label.pack()

        self.canvas=tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.draw_wheel()

        self.pointer=self.canvas.create_polygon(250, 50, 230, 70, 270, 70, fill="black")
    def draw_wheel(self):
        cx, cy=250,250
        radius=200
        num_segments=len(self.numbers)
        self.canvas.delete("wheel")
        for i, (number, color) in enumerate(self.numbers):
            start_angle=(i*(360 / num_segments)) + self.rotation_angle
            end_angle=(360/num_segments)

            self.canvas.create_arc(
                cx-radius, cy-radius, cx+radius, cy+radius,
                start=start_angle, extent=end_angle,
                fill=color, outline="black", tag="wheel"
            )
            angle_rad=math.radians(start_angle+end_angle/2)
            x=cx+(radius-30)*math.cos(angle_rad)
            y=cy-(radius-30)*math.sin(angle_rad)
            self.canvas.create_text(x, y, text=str(number), fill="white", font=("Arial", 12), tag="wheel")

    def auto_bet(self):
        if self.loss_streak>=self.max_loss_streak:
            self.result_label.config(text="Stopped due to 12 consecutive losses")
            return
        self.result_label.config(text="Spinning...", fg="blue")
        self.root.update()

        for _ in range(30):
            self.rotation_angle+=12
            self.draw_wheel()
            self.root.update()
            time.sleep(0.05)
        self.result_number, result_color=random.choice(self.numbers)
        self.rotation_angle=(self.rotation_angle++random.randint(1, 20))%360

        self.result_label.config(text=f"Number: {self.result_number} ({result_color.capitalize()})",
                fg="green" if self.selected_color==result_color else "red")

        if result_color==self.selected_color:
            self.balance+=self.bet_amount
            self.result_label.config(fg="green")
            self.loss_streak=0
            self.bet_amount=1
        else:
            self.balance-=self.bet_amount
            self.loss_streak+=1
            self.bet_amount*=2

        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_label.config(text=f"Betting on {self.selected_color}, amount: {self.bet_amount}")

        self.root.after(1000, self.auto_bet)

        self.log(self.bet_amount, self.result_number, result_color)


    def log(self, bet_amount, result_number, result_color):
        with open("trans.txt", "a") as file:
            file.write(f"Bet: {self.bet_amount}, Result: {result_number} {result_color.capitalize()}), Balance: ${self.balance}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = roulette(root)
    root.mainloop()
