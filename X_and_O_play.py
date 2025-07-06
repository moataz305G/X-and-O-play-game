#import tkinter lirarre
import tkinter as tk
import random

root = tk.Tk()
root.title("Welcome to game X and O")
root.geometry("600x600")
root.grid_columnconfigure(0, weight=1)

your_score = 0
computer_score = 0

Control_panel = [""] * 9
current_player = "X"
# frame1
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, pady=20)

score_label = tk.Label(frame1, text=f"You : {your_score}  Computer : {computer_score}", font=("Arial", 25))
score_label.grid(row=0, column=0)

win_lose_label = tk.Label(frame1, text="", font=("Arial", 25))
win_lose_label.grid(row=1, column=0, pady=10)

def restart_game():
    global Control_panel, current_player
    Control_panel = [""] * 9
    current_player = "X"
    for button in buttons:
        button.config(text="", bg="lightgray", state=tk.NORMAL)
    win_lose_label.config(text="")

Restart_Button = tk.Button(frame1, text="Restart", font=("Arial", 18), command=restart_game)
Restart_Button.grid(row=2, column=0)
# frame2
frame2 = tk.Frame(root)
frame2.grid(row=1, column=0)

buttons = []

def check_winner(player):
    win_condition = [
        [0,1,2], [3,4,5], [6,7,8],  # صفوف
        [0,3,6], [1,4,7], [2,5,8],  # أعمدة
        [0,4,8], [2,4,6]            # أقطار
    ]
    for condition in win_condition:
        if all(Control_panel[i] == player for i in condition):
            return True
    return False

def computer_move():
    empty_cells = [i for i in range(9) if Control_panel[i] == ""]
    if empty_cells:
        choice = random.choice(empty_cells)
        Control_panel[choice] = "O"
        buttons[choice].config(text="O")

def button_click(index):
    global your_score, computer_score, current_player

    if Control_panel[index] == "":
        Control_panel[index] = current_player
        buttons[index].config(text=current_player, bg="skyblue")

        if check_winner(current_player):
            win_lose_label.config(text=f"{current_player} Wins!")
            for btn in buttons:
                btn.config(state=tk.DISABLED)
            if current_player == "X":
                your_score += 1
            else:
                computer_score += 1
            update_score()
            return

        if "" not in Control_panel:   # تعادل
            win_lose_label.config(text="Tie, No Winner!")
            for btn in buttons:
                btn.config(bg="red")
            return

        #   تغيير الدور إلى الكمبيوتر
        current_player = "O"
        computer_move()

        if check_winner("O"):
            win_lose_label.config(text="Computer Wins!")
            for btn in buttons:
                btn.config(state=tk.DISABLED)
            computer_score += 1
            update_score()
            return

        if "" not in Control_panel:   # تعادل   
            win_lose_label.config(text="Tie, No Winner!")
            for btn in buttons:
                btn.config(bg="red")
            return

        current_player = "X"

def update_score():
    score_label.config(text=f"You : {your_score}  Computer : {computer_score}", font=("Arial", 25))

for i in range(9):
    button = tk.Button(frame2, text="", font=("Arial", 31), width=7, height=2,
                       command=lambda i=i: button_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

root.mainloop()
