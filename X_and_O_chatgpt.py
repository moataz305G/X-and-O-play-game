import tkinter as tk
import random

root = tk.Tk()
root.title("welcom to game X and O")
root.geometry("650x650")
root.resizable(False, False)
root.grid_columnconfigure(0, weight=1)

current_player = "X"  # X هو اللاعب الأول
player_score = 0
computer_score = 0
mode = None  # سيتم تحديده لاحقًا بناءً على اختيار المستخدم
buttons = []
time_left = 11
timer_id = None
player1_name = "Player 1"
player2_name = "Player 2"
game_over = False

# ===== واجهة البداية =====
start_frame = tk.Frame(root)
start_frame.pack(expand=True)

start_label = tk.Label(start_frame, text="Welcome to the game X O\nChoose Game Mode:", font=("Arial", 16))
start_label.pack(pady=20)

def open_pvp_name_input():
    start_frame.pack_forget()
    pvp_frame.pack(expand=True)

def open_ai_level_select():
    start_frame.pack_forget()
    ai_frame.pack(expand=True)

pvp_btn = tk.Button(start_frame, text="Player vs Player", command=open_pvp_name_input, font=("Arial", 14))
pvp_btn.pack(pady=5)
ai_btn = tk.Button(start_frame, text="Player vs Computer", command=open_ai_level_select, font=("Arial", 14))
ai_btn.pack(pady=5)

# ===== واجهة PvP لاختيار الأسماء =====
pvp_frame = tk.Frame(root)
pvp_label = tk.Label(pvp_frame, text="Enter Player Names:", font=("Arial", 16))
pvp_label.pack(pady=10)

player1_entry = tk.Entry(pvp_frame, font=("Arial", 14))
player1_entry.pack(pady=5)
player1_entry.insert(0, "Player 1")

player2_entry = tk.Entry(pvp_frame, font=("Arial", 14))
player2_entry.pack(pady=5)
player2_entry.insert(0, "Player 2")

def set_pvp_mode():
    global mode, player1_name, player2_name
    mode = "PvP"
    player1_name = player1_entry.get()
    player2_name = player2_entry.get()
    pvp_frame.pack_forget()
    build_game()

pvp_start_btn = tk.Button(pvp_frame, text="Start PvP Game", command=set_pvp_mode, font=("Arial", 14))
pvp_start_btn.pack(pady=10)
back_btn_pvp = tk.Button(pvp_frame, text="Back", command=lambda:[pvp_frame.pack_forget(), start_frame.pack(expand=True)], font=("Arial", 14))
back_btn_pvp.pack(pady=5)

# =====  واجهة اختيار مستوى الذكاء الاصطناعي  =====
ai_frame = tk.Frame(root)
ai_label1 = tk.Label(ai_frame, text="your name: ", font=("Arial", 16))
ai_label1.grid(row=0,column=0,pady=5)

ai_player1_entry = tk.Entry(ai_frame, font=("Arial", 14))
ai_player1_entry.grid(row=0,column=1,pady=5)
ai_player1_entry.insert(0, "Player ")

ai_label = tk.Label(ai_frame, text="Select your Level:", font=("Arial", 16))
ai_label.grid(row=1,column=1,pady=10)

def set_ai_mode(selected_mode):
    global mode ,player1_name
    mode = selected_mode
    player1_name = ai_player1_entry.get()
    ai_frame.pack_forget()
    build_game()

tk.Button(ai_frame, text="Easy", command=lambda: set_ai_mode("Easy"), font=("Arial", 16)).grid(row=2,column=1,pady=5)
tk.Button(ai_frame, text="Medium", command=lambda: set_ai_mode("Medium"), font=("Arial", 16)).grid(row=3,column=1,pady=5)
tk.Button(ai_frame, text="Impossible", command=lambda: set_ai_mode("Impossible"), font=("Arial", 16)).grid(row=4,column=1,pady=5)
back_btn_ai = tk.Button(ai_frame, text="Back", command=lambda:[ai_frame.pack_forget(), start_frame.pack(expand=True)], font=("Arial", 14))
back_btn_ai.grid(row=5,column=1,pady=5) 

# ===== بناء اللعبة =====
def build_game():
    global score_label, match_result_label, timer_label

    score_label = tk.Label(root, text=f"{player1_name} : {player_score}  {player2_name if mode=='PvP' else 'Computer'} : {computer_score}", font=("Arial", 16))
    score_label.pack(pady=10)

    match_result_label = tk.Label(root, text="", font=("Arial", 14))
    match_result_label.pack(pady=5)

    timer_label = tk.Label(root, text=f"Time: {time_left}", font=("Arial", 14))
    timer_label.pack(pady=5)

    frame = tk.Frame(root)
    frame.pack()

    for i in range(9):
        button = tk.Button(frame, text="", font=("Arial", 24), width=5, height=2,
                           command=lambda i=i: button_click(i))
        button.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(button)

    restart_btn = tk.Button(root, text="Restart", font=("Arial", 16), command=restart_game)
    restart_btn.pack(pady=10)

    start_timer()

def start_timer():
    global time_left, timer_id
    if timer_id:
        root.after_cancel(timer_id)
    time_left = 10
    timer_count()

def timer_count():
    global time_left, timer_id, game_over
    if game_over:
        return
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time: {time_left}")
        timer_id = root.after(1000, timer_count)
    else:
        switch_player_on_timeout()

def switch_player_on_timeout():
    global current_player
    empty = [i for i, b in enumerate(buttons) if b['text'] == ""]
    if empty:
        choice = random.choice(empty)
        buttons[choice].config(text=current_player, bg="lightblue" if current_player == "X" else "lightgreen")
        winner, combo = check_winner()
        if winner:
            end_game(winner, combo)
            return
        elif all(b['text'] != "" for b in buttons):
            draw()
            return
    if mode == "PvP":
        current_player = "O" if current_player == "X" else "X"
        start_timer()
    elif mode.startswith("Easy") or mode.startswith("Medium") or mode.startswith("Impossible"):
        current_player = "O"
        root.after(500, computer_play_after_timeout)

def computer_play_after_timeout():
    global current_player
    if mode.startswith("Easy") or mode.startswith("Medium") or mode.startswith("Impossible"):
        ai_index = ai_move()
        if ai_index is not None:
            buttons[ai_index].config(text="O", bg="lightgreen")
            winner, combo = check_winner()
            if winner:
                end_game(winner, combo)
                return
            elif all(b['text'] != "" for b in buttons):
                draw()
                return
        current_player = "X"
        start_timer()

def ai_move():
    if mode == "Easy":
        empty = [i for i, b in enumerate(buttons) if b['text'] == ""]
        return random.choice(empty) if empty else None
    elif mode == "Medium":
        for mark in ["O", "X"]:
            for i in range(9):
                if buttons[i]['text'] == "":
                    buttons[i]['text'] = mark
                    winner, _ = check_winner()
                    buttons[i]['text'] = ""
                    if winner == mark:
                        return i
        empty = [i for i, b in enumerate(buttons) if b['text'] == ""]
        return random.choice(empty) if empty else None
    elif mode == "Impossible":
        return minimax_move()

def minimax_move():
    best_score = -float('inf')
    best_move = None
    for i in range(9):
        if buttons[i]['text'] == "":
            buttons[i]['text'] = "O"
            score = minimax(False)
            buttons[i]['text'] = ""
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

def minimax(is_maximizing):
    winner, _ = check_winner()
    if winner == "O": return 1
    if winner == "X": return -1
    if all(button['text'] != "" for button in buttons): return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if buttons[i]['text'] == "":
                buttons[i]['text'] = "O"
                score = minimax(False)
                buttons[i]['text'] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if buttons[i]['text'] == "":
                buttons[i]['text'] = "X"
                score = minimax(True)
                buttons[i]['text'] = ""
                best_score = min(score, best_score)
        return best_score

def button_click(index):
    global current_player, game_over

    if buttons[index]['text'] == "" and (mode == "PvP" or current_player == "X"):
        buttons[index]['text'] = current_player
        buttons[index].config(bg="lightblue" if current_player == "X" else "lightgreen")

        winner, combo = check_winner()
        if winner:
            end_game(winner, combo)
            return
        elif all(button['text'] != "" for button in buttons):
            draw()
            return

        if mode == "PvP":
            current_player = "O" if current_player == "X" else "X"
            start_timer()
        else:
            current_player = "O"
            ai_index = ai_move()
            if ai_index is not None:
                buttons[ai_index].config(text="O", bg="lightgreen")
                winner, combo = check_winner()
                if winner:
                    end_game(winner, combo)
                    return
                elif all(b['text'] != "" for b in buttons):
                    draw()
                    return
            current_player = "X"
            start_timer()

def check_winner():
    combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in combos:
        if buttons[combo[0]]['text'] == buttons[combo[1]]['text'] == buttons[combo[2]]['text'] != "":
            return buttons[combo[0]]['text'], combo
    return None, None

def end_game(winner, combo):
    global player_score, computer_score, game_over
    game_over = True
    if winner == "X":
        player_score += 1
        match_result_label.config(text=f"{player1_name} wins!")
    else:
        computer_score += 1
        match_result_label.config(text=f"{player2_name if mode=='PvP' else 'Computer'} wins!")

    for i in combo:
        buttons[i].config(bg="orange")
    update_score()
    disable_buttons()

def draw():
    global game_over
    game_over = True
    match_result_label.config(text="Draw!")
    for button in buttons:
        button.config(bg="red")
    disable_buttons()

def update_score():
    score_label.config(text=f"{player1_name} : {player_score}  {player2_name if mode=='PvP' else 'Computer'} : {computer_score}")

def disable_buttons():
    for button in buttons:
        button.config(state="disabled")

def restart_game():
    global current_player, timer_id, game_over
    current_player = "X"
    game_over = False
    if timer_id:
        root.after_cancel(timer_id)
    for button in buttons:
        button.config(text="", bg="lightgray", state="normal")
    match_result_label.config(text="")
    start_timer()

root.mainloop()
