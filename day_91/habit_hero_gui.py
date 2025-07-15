import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = 'habit_hero_gui_data.json'
DEFAULT_HABITS = [
    'Brush teeth',
    'Read a book',
    'Help at home',
    'Drink water',
    'Exercise',
]
REWARDS = [
    (3, 'Bronze Star ⭐'),
    (7, 'Silver Badge 🥈'),
    (14, 'Gold Medal 🥇'),
    (30, 'Diamond Trophy 💎'),
]

# Data functions
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'habits': DEFAULT_HABITS, 'progress': {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_streak(dates):
    if not dates:
        return 0
    dates = sorted([datetime.strptime(d, '%Y-%m-%d') for d in dates], reverse=True)
    streak = 1
    for i in range(1, len(dates)):
        if (dates[i-1] - dates[i]).days == 1:
            streak += 1
        else:
            break
    return streak

# GUI App
class HabitHeroApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Habit Hero: The Streak Adventure')
        self.root.geometry('500x500')
        self.root.configure(bg='#f0e6ff')
        self.data = load_data()
        self.main_frame = tk.Frame(self.root, bg='#f0e6ff')
        self.main_frame.pack(fill='both', expand=True)
        self.show_home()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_frame()
        tk.Label(self.main_frame, text='🦸‍♂️ Habit Hero', font=('Comic Sans MS', 28, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=20)
        tk.Label(self.main_frame, text='Build awesome habits and earn rewards!', font=('Comic Sans MS', 14), bg='#f0e6ff').pack(pady=10)
        tk.Button(self.main_frame, text='Start', font=('Comic Sans MS', 16, 'bold'), bg='#a3e635', fg='#222', command=self.show_habits).pack(pady=20)
        tk.Button(self.main_frame, text='Exit', font=('Comic Sans MS', 12), command=self.root.quit).pack(pady=10)

    def show_habits(self):
        self.clear_frame()
        tk.Label(self.main_frame, text='Your Habits', font=('Comic Sans MS', 20, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=10)
        for habit in self.data['habits']:
            tk.Label(self.main_frame, text=f'• {habit}', font=('Comic Sans MS', 14), bg='#f0e6ff').pack(anchor='w', padx=40)
        tk.Button(self.main_frame, text='Add Habit', font=('Comic Sans MS', 12), bg='#fbbf24', command=self.add_habit).pack(pady=5)
        tk.Button(self.main_frame, text='Daily Check-in', font=('Comic Sans MS', 14, 'bold'), bg='#38bdf8', command=self.show_checkin).pack(pady=10)
        tk.Button(self.main_frame, text='Show Progress & Rewards', font=('Comic Sans MS', 12), bg='#a3e635', command=self.show_progress).pack(pady=5)
        tk.Button(self.main_frame, text='Back to Home', font=('Comic Sans MS', 12), command=self.show_home).pack(pady=10)

    def add_habit(self):
        new_habit = simpledialog.askstring('Add Habit', 'Enter a new habit:')
        if new_habit and new_habit.strip() and new_habit not in self.data['habits']:
            self.data['habits'].append(new_habit.strip())
            save_data(self.data)
            messagebox.showinfo('Habit Added', f"'{new_habit}' added!")
            self.show_habits()
        else:
            messagebox.showwarning('Invalid', 'Please enter a unique, non-empty habit.')

    def show_checkin(self):
        self.clear_frame()
        tk.Label(self.main_frame, text='Daily Check-in', font=('Comic Sans MS', 20, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=10)
        today = datetime.now().strftime('%Y-%m-%d')
        self.checkin_vars = {}
        for habit in self.data['habits']:
            var = tk.BooleanVar()
            prev_done = today in self.data['progress'].get(habit, [])
            var.set(prev_done)
            cb = tk.Checkbutton(self.main_frame, text=habit, font=('Comic Sans MS', 14), bg='#f0e6ff', variable=var)
            cb.pack(anchor='w', padx=40)
            self.checkin_vars[habit] = var
        tk.Button(self.main_frame, text='Submit', font=('Comic Sans MS', 14, 'bold'), bg='#38bdf8', command=self.submit_checkin).pack(pady=15)
        tk.Button(self.main_frame, text='Back', font=('Comic Sans MS', 12), command=self.show_habits).pack(pady=5)

    def submit_checkin(self):
        today = datetime.now().strftime('%Y-%m-%d')
        for habit, var in self.checkin_vars.items():
            if var.get():
                if habit not in self.data['progress']:
                    self.data['progress'][habit] = []
                if today not in self.data['progress'][habit]:
                    self.data['progress'][habit].append(today)
        save_data(self.data)
        messagebox.showinfo('Check-in Complete', 'Great job! Keep up the good habits!')
        self.show_habits()

    def show_progress(self):
        self.clear_frame()
        tk.Label(self.main_frame, text='Your Streaks & Rewards', font=('Comic Sans MS', 20, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=10)
        for habit in self.data['habits']:
            streak = get_streak(self.data['progress'].get(habit, []))
            reward = ''
            for days, r in reversed(REWARDS):
                if streak >= days:
                    reward = r
                    break
            streak_text = f"{habit}: {streak} day streak"
            if reward:
                streak_text += f"  |  Reward: {reward}"
            tk.Label(self.main_frame, text=streak_text, font=('Comic Sans MS', 14), bg='#f0e6ff').pack(anchor='w', padx=40, pady=2)
        tk.Button(self.main_frame, text='Back', font=('Comic Sans MS', 12), command=self.show_habits).pack(pady=15)

if __name__ == '__main__':
    root = tk.Tk()
    app = HabitHeroApp(root)
    root.mainloop() 