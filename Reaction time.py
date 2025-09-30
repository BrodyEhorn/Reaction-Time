import time
import tkinter as tk
import random
import sqlite3
from tkinter import simpledialog


global state, running
#0: waiting to start
#1: waiting to click
#2: clicked, show time
#3: show time, waiting to reset or click too soon, reset
state = 0
running = False

conn = sqlite3.connect("leaderboard.db")
cursor = conn.cursor()

def handle_click(event):
    global state, running, timer_job
    if state == 0:
        start_timer()
    elif state == 1:
        time_label.config(text="Too soon! Click to reset")
        root.config(bg="light coral")
        time_label.config(bg="light coral")
        state = 3
        running = False
        if timer_job:
            root.after_cancel(timer_job)
            timer_job = None
    elif state == 2:
        global start_time
        reaction_time = time.time() - start_time
        time_label.config(text=f"Reaction time: {reaction_time:.3f} seconds\nClick to reset")
        root.config(bg="white")
        time_label.config(bg="white")
        running = False
        state = 3

        cursor.execute("SELECT reaction_time FROM scores ORDER BY reaction_time ASC LIMIT 5")
        top_scores = [row[0] for row in cursor.fetchall()]

        # If leaderboard has fewer than 5, always qualifies
        if len(top_scores) < 5 or reaction_time < max(top_scores):
            player_name = simpledialog.askstring("New High Score!", "You made the leaderboard!\n Enter your name:")
        if not player_name:
            player_name = "Anonymous"



        cursor.execute(
            "INSERT INTO scores (name, reaction_time) VALUES (?, ?)",
            (player_name, reaction_time)
        )
        conn.commit()
        update_leaderboard()


    elif state == 3:
        state = 0
        time_label.config(text="Click to start")
        root.config(bg="white")
        time_label.config(bg="white")
        leaderboard_label.pack(pady=20)

def start_timer():
    global state, running, timer_job
    if not running:
        state = 1
        running = True
        time_label.config(text="Wait...")
        root.config(bg="#ffe799")
        time_label.config(bg="#ffe799")

        leaderboard_label.pack_forget()

        delay = random.randint(1500, 2500) 
        timer_job = root.after(delay, click_signal)

        running = True

def click_signal():
    global state, start_time
    if(state == 1):
        state = 2
        start_time = time.time()
        time_label.config(text="Click!")
        root.config(bg="pale green")
        time_label.config(bg="pale green")

def update_leaderboard():
    cursor.execute("SELECT name, reaction_time FROM scores ORDER BY reaction_time ASC LIMIT 5")
    top_scores = cursor.fetchall()
    leaderboard_text = "Leaderboard:\n"
    for i, (name, reaction_time) in enumerate(top_scores, start=1):
        leaderboard_text += f"{i}. {name}: {reaction_time:.3f}\n"
    leaderboard_label.config(text=leaderboard_text)
       

root = tk.Tk()
root.title("Reaction time")
root.geometry("400x500")
root.config(bg="white")
root.bind("<Button-1>", handle_click)

time_label = tk.Label(root, text="Click to start", font=("Helvetica", 30), wraplength=300, justify="center")
time_label.pack(pady=50)

leaderboard_label = tk.Label(root, text="Leaderboard:\n", font=("Helvetica", 16), justify="left", bg="white")
leaderboard_label.pack(pady=20)

update_leaderboard()




cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        reaction_time REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()



# Start the Tkinter event loop
root.mainloop()