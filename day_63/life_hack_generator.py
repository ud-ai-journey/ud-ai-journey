import random
import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

# Expanded list of life hacks, including one for energetic states
hacks = [
    "Use the 5-Minute Rule: Start a task for just 5 minutes to beat procrastination.",
    "Try the 2-Minute Rule: If a task takes less than 2 minutes, do it immediately.",
    "Break tasks into 3 tiny steps. Complete one to build momentum.",
    "Change your environment: A new setting can spark fresh motivation.",
    "Do a 25-minute Pomodoro sprint with no distractions. Reward yourself after!",
    "Feeling stressed? Take 10 deep breaths and focus on the exhale.",
    "Write down 3 things you're grateful for to shift your mindset.",
    "Set a timer for 10 minutes to declutter one area—it’s a quick win!",
    "Drink a glass of water to boost energy and focus instantly.",
    "Use the 'One Touch Rule': Handle each item once to avoid clutter pile-up.",
    "Feeling overwhelmed? List your tasks and tackle the easiest one first.",
    "Play upbeat music for 2 minutes to lift your mood before starting work.",
    "Schedule a 5-minute 'worry time' to contain stress, then move on.",
    "Stand up and stretch for 30 seconds to reset your body and mind.",
    "Visualize completing your task successfully to boost confidence.",
    "You're feeling energetic? Channel that energy into a quick win—tackle a task you've been avoiding!"
]

# Function to save input and hack to log.txt
def save_to_log(user_input, hack):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Problem: {user_input}\nSolution: {hack}\n\n"
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log_entry)

# Function to match input to a hack
def get_life_hack(user_input):
    user_input = user_input.lower().strip()
    if not user_input:
        return "No problem entered. Try typing something like 'I'm stressed' or 'I procrastinate a lot'."
    
    # Improved keyword detection with energetic state
    if any(word in user_input for word in ["energetic", "energized", "active", "motivated"]):
        hack = hacks[15]  # Energetic-specific hack
    elif any(word in user_input for word in ["lazy", "tired", "unmotivated", "no energy"]):
        hack = hacks[0] if "procrastinate" in user_input else hacks[8]  # 5-Minute Rule or drink water
    elif any(word in user_input for word in ["procrastinate", "putting off", "delay"]):
        hack = hacks[0]  # 5-Minute Rule
    elif any(word in user_input for word in ["stress", "anxious", "overwhelm"]):
        hack = hacks[5] if "stress" in user_input else hacks[10]  # Deep breaths or tackle easiest task
    elif any(word in user_input for word in ["fear", "scared", "nervous"]):
        hack = hacks[14]  # Visualize success
    elif any(word in user_input for word in ["messy", "clutter", "disorganized"]):
        hack = hacks[7]  # Declutter for 10 minutes
    elif any(word in user_input for word in ["sad", "down", "depressed"]):
        hack = hacks[6]  # Gratitude list
    else:
        hack = random.choice(hacks)  # Random hack for unmatched input
    
    # Save to log
    save_to_log(user_input, hack)
    return hack

# GUI with tkinter
class LifeHackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI-Powered Life Hack Generator")
        self.root.geometry("400x300")
        
        # Label
        self.label = tk.Label(root, text="What's bothering you today?", font=("Arial", 12))
        self.label.pack(pady=10)
        
        # Text entry
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)
        
        # Button
        self.button = tk.Button(root, text="Get Life Hack", command=self.show_hack)
        self.button.pack(pady=10)
        
        # Output label
        self.output = tk.Label(root, text="", font=("Arial", 10), wraplength=350, justify="center")
        self.output.pack(pady=10)
        
    def show_hack(self):
        user_input = self.entry.get()
        hack = get_life_hack(user_input)
        self.output.config(text=hack)
        messagebox.showinfo("Your Life Hack", hack)

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = LifeHackApp(root)
    root.mainloop()