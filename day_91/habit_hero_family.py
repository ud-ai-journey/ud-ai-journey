import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os
from datetime import datetime

HABIT_LIBRARY_FILE = 'day_91/habits_library.json'
DATA_FILE = 'habit_hero_family_data.json'
ASSETS_DIR = 'day_91/assets/'

# Load habit library
with open(HABIT_LIBRARY_FILE, 'r') as f:
    HABIT_LIBRARY = json.load(f)

# Data functions
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'kids': {}}

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

class HabitHeroFamilyApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Habit Hero Family Edition')
        self.root.geometry('900x600')
        self.data = load_data()
        self.selected_kid = None
        self.main_frame = tk.Frame(self.root, bg='#f0e6ff')
        self.main_frame.pack(fill='both', expand=True)
        self.drag_data = {'widget': None, 'item': None}
        self.show_profile_select()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_profile_select(self):
        self.clear_frame()
        tk.Label(self.main_frame, text='👨‍👩‍👧‍👦 Habit Hero Family', font=('Comic Sans MS', 28, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=20)
        tk.Label(self.main_frame, text='Select or add a child profile:', font=('Comic Sans MS', 16), bg='#f0e6ff').pack(pady=10)
        for kid in self.data['kids']:
            tk.Button(self.main_frame, text=kid, font=('Comic Sans MS', 14), width=20, command=lambda k=kid: self.select_kid(k)).pack(pady=5)
        tk.Button(self.main_frame, text='+ Add Child', font=('Comic Sans MS', 14), bg='#a3e635', command=self.add_kid).pack(pady=10)

    def add_kid(self):
        name = simpledialog.askstring('Add Child', 'Enter child name:')
        if name and name.strip() and name not in self.data['kids']:
            self.data['kids'][name] = {'assigned_habits': [], 'progress': {}}
            save_data(self.data)
            self.show_profile_select()
        else:
            messagebox.showwarning('Invalid', 'Please enter a unique, non-empty name.')

    def select_kid(self, kid):
        self.selected_kid = kid
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Parent Dashboard – {self.selected_kid}", font=('Comic Sans MS', 22, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=10)
        # Search box
        tk.Label(self.main_frame, text='Search Habits:', font=('Comic Sans MS', 12), bg='#f0e6ff').place(x=40, y=30)
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_habit_library)
        search_entry = tk.Entry(self.main_frame, textvariable=self.search_var, font=('Comic Sans MS', 12), width=30)
        search_entry.place(x=150, y=30)
        # Habit Library Listbox
        tk.Label(self.main_frame, text='Habit Library', font=('Comic Sans MS', 14, 'bold'), bg='#f0e6ff').place(x=40, y=60)
        self.library_listbox = tk.Listbox(self.main_frame, width=35, height=20, font=('Comic Sans MS', 12))
        self.library_listbox.place(x=40, y=90)
        self.filtered_habits = HABIT_LIBRARY.copy()
        self.update_habit_library()
        # Assigned Habits Listbox
        tk.Label(self.main_frame, text="Today's Board", font=('Comic Sans MS', 14, 'bold'), bg='#f0e6ff').place(x=350, y=60)
        self.board_listbox = tk.Listbox(self.main_frame, width=35, height=20, font=('Comic Sans MS', 12))
        for habit in self.data['kids'][self.selected_kid]['assigned_habits']:
            self.board_listbox.insert('end', habit)
        self.board_listbox.place(x=350, y=90)
        # Drag-and-drop bindings
        self.library_listbox.bind('<ButtonPress-1>', self.on_start_drag)
        self.library_listbox.bind('<B1-Motion>', self.on_drag_motion)
        self.library_listbox.bind('<ButtonRelease-1>', self.on_drop)
        self.board_listbox.bind('<Enter>', self.on_board_enter)
        self.board_listbox.bind('<Leave>', self.on_board_leave)
        # Remove habit by double-click
        self.board_listbox.bind('<Double-Button-1>', self.on_remove_habit)
        # Switch to Kid's Board
        tk.Button(self.main_frame, text="Go to Kid's Board", font=('Comic Sans MS', 14, 'bold'), bg='#a3e635', command=self.show_kid_board).place(x=650, y=120)
        tk.Button(self.main_frame, text='Switch Child', font=('Comic Sans MS', 12), command=self.show_profile_select).place(x=650, y=180)
        tk.Button(self.main_frame, text='Exit', font=('Comic Sans MS', 12), command=self.root.quit).place(x=650, y=240)
        # Drag label
        self.drag_label = tk.Label(self.main_frame, text='', font=('Comic Sans MS', 12, 'bold'), bg='#f0e6ff', fg='#38bdf8')

    def update_habit_library(self, *args):
        search = self.search_var.get().lower() if hasattr(self, 'search_var') else ''
        self.library_listbox.delete(0, 'end')
        self.filtered_habits = [h for h in HABIT_LIBRARY if search in h['name'].lower() or search in h['category'].lower()]
        for habit in self.filtered_habits:
            self.library_listbox.insert('end', f"{habit['name']}  [{habit['category']}]" )

    def on_start_drag(self, event):
        idx = self.library_listbox.nearest(event.y)
        if idx >= 0:
            self.drag_data['item'] = self.library_listbox.get(idx)
            self.drag_label.config(text=f"Dragging: {self.drag_data['item']}")
            self.drag_label.place(x=event.x_root - self.root.winfo_rootx(), y=event.y_root - self.root.winfo_rooty())

    def on_drag_motion(self, event):
        if self.drag_data['item']:
            self.drag_label.place(x=event.x_root - self.root.winfo_rootx(), y=event.y_root - self.root.winfo_rooty())

    def on_drop(self, event):
        if self.drag_data['item']:
            # Check if drop is over the board_listbox
            x, y = event.x_root - self.root.winfo_rootx(), event.y_root - self.root.winfo_rooty()
            bx, by, bw, bh = self.board_listbox.winfo_x(), self.board_listbox.winfo_y(), self.board_listbox.winfo_width(), self.board_listbox.winfo_height()
            if bx <= x <= bx + bw and by <= y <= by + bh:
                # Drop on board
                if self.drag_data['item'] not in self.data['kids'][self.selected_kid]['assigned_habits']:
                    self.data['kids'][self.selected_kid]['assigned_habits'].append(self.drag_data['item'])
                    save_data(self.data)
                    self.show_dashboard()
                else:
                    messagebox.showinfo('Already assigned', 'This habit is already on the board.')
            self.drag_label.place_forget()
            self.drag_data = {'widget': None, 'item': None}

    def on_board_enter(self, event):
        self.board_listbox.config(bg='#d1fae5')

    def on_board_leave(self, event):
        self.board_listbox.config(bg='white')

    def on_remove_habit(self, event):
        idx = self.board_listbox.nearest(event.y)
        if idx >= 0:
            habit_text = self.board_listbox.get(idx)
            self.data['kids'][self.selected_kid]['assigned_habits'].remove(habit_text)
            save_data(self.data)
            self.show_dashboard()

    def show_kid_board(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"{self.selected_kid}'s Board", font=('Comic Sans MS', 22, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=10)
        today = datetime.now().strftime('%Y-%m-%d')
        assigned = self.data['kids'][self.selected_kid]['assigned_habits']
        self.checkin_vars = {}
        for idx, habit in enumerate(assigned):
            var = tk.BooleanVar()
            prev_done = today in self.data['kids'][self.selected_kid]['progress'].get(habit, [])
            var.set(prev_done)
            cb = tk.Checkbutton(self.main_frame, text=habit, font=('Comic Sans MS', 14), bg='#f0e6ff', variable=var)
            cb.pack(anchor='w', padx=60)
            self.checkin_vars[habit] = var
        tk.Button(self.main_frame, text='Submit Check-in', font=('Comic Sans MS', 14, 'bold'), bg='#38bdf8', command=self.submit_checkin).pack(pady=15)
        tk.Button(self.main_frame, text='Show Streaks', font=('Comic Sans MS', 12), bg='#a3e635', command=self.show_streaks).pack(pady=5)
        tk.Button(self.main_frame, text='Back to Dashboard', font=('Comic Sans MS', 12), command=self.show_dashboard).pack(pady=5)

    def submit_checkin(self):
        today = datetime.now().strftime('%Y-%m-%d')
        for habit, var in self.checkin_vars.items():
            if var.get():
                if habit not in self.data['kids'][self.selected_kid]['progress']:
                    self.data['kids'][self.selected_kid]['progress'][habit] = []
                if today not in self.data['kids'][self.selected_kid]['progress'][habit]:
                    self.data['kids'][self.selected_kid]['progress'][habit].append(today)
        save_data(self.data)
        messagebox.showinfo('Check-in Complete', 'Great job! Keep up the good habits!')
        self.show_kid_board()

    def show_streaks(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"{self.selected_kid}'s Streaks", font=('Comic Sans MS', 22, 'bold'), bg='#f0e6ff', fg='#6c3eb6').pack(pady=10)
        for habit in self.data['kids'][self.selected_kid]['assigned_habits']:
            streak = get_streak(self.data['kids'][self.selected_kid]['progress'].get(habit, []))
            tk.Label(self.main_frame, text=f"{habit}: {streak} day streak", font=('Comic Sans MS', 14), bg='#f0e6ff').pack(anchor='w', padx=60)
        tk.Button(self.main_frame, text='Back to Board', font=('Comic Sans MS', 12), command=self.show_kid_board).pack(pady=15)

if __name__ == '__main__':
    root = tk.Tk()
    app = HabitHeroFamilyApp(root)
    root.mainloop() 