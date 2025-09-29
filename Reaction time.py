import time
import tkinter as tk


global state, running
#0: waiting to start
#1: waiting to click
#2: clicked, show time
state = 0
running = False

def handle_click(event):
    global state, running, timer_job
    if state == 0:
        start_timer()
    elif state == 1:
        time_label.config(text="Too soon! Click to try again")
        root.config(bg="light coral")
        time_label.config(bg="light coral")
        state = 0
        running = False
        if timer_job:
            root.after_cancel(timer_job)
            timer_job = None
    elif state == 2:
        global start_time
        reaction_time = time.time() - start_time
        time_label.config(text=f"Reaction time: {reaction_time:.3f} seconds\nClick to try again")
        root.config(bg="white")
        time_label.config(bg="white")
        running = False
        state = 0

def start_timer():
    global state, running, timer_job
    if not running:
        state = 1
        running = True
        time_label.config(text="Wait for green")
        root.config(bg="#ffe799")
        time_label.config(bg="#ffe799")
        timer_job = root.after(2000, click_signal)
        running = True

def click_signal():
    global state, start_time
    if(state == 1):
        state = 2
        start_time = time.time()
        time_label.config(text="Click!")
        root.config(bg="pale green")
        time_label.config(bg="pale green")
       


root = tk.Tk()
root.title("Reaction time")
root.geometry("400x500")
root.bind("<Button-1>", handle_click)

time_label = tk.Label(root, text="Click to start", font=("Helvetica", 30), wraplength=300, justify="center")
time_label.pack(pady=50)


# Start the Tkinter event loop
root.mainloop()