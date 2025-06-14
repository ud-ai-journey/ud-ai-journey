import tkinter as tk
from tkinter import ttk, scrolledtext, font
import threading
from voice_assistant import VoiceAssistant
import time
from datetime import datetime

class VoiceAssistantGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#2C3E50')  # Dark blue background
        
        # Initialize voice assistant
        self.assistant = VoiceAssistant()
        self.is_listening = False
        self.stop_listening = False
        
        self.setup_gui()
        
    def setup_gui(self):
        # Title frame
        title_frame = tk.Frame(self.root, bg='#2C3E50')
        title_frame.pack(pady=20)
        
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title = tk.Label(title_frame, text="🤖 Voice Assistant", font=title_font,
                        bg='#2C3E50', fg='white')
        title.pack()
        
        status_font = font.Font(family="Helvetica", size=10)
        self.status_label = tk.Label(title_frame, text="Ready to help!",
                                   font=status_font, bg='#2C3E50', fg='#3498DB')
        self.status_label.pack(pady=5)
        
        # Chat display
        chat_frame = tk.Frame(self.root, bg='#34495E', padx=10, pady=10)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, width=50, height=20,
            font=("Helvetica", 11), bg='#ECF0F1', fg='#2C3E50')
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons frame
        button_frame = tk.Frame(self.root, bg='#2C3E50')
        button_frame.pack(pady=20)
        
        # Custom button style
        button_style = {
            'font': ('Helvetica', 12),
            'width': 15,
            'height': 2,
            'bd': 0,
            'borderwidth': 0,
            'relief': 'flat',
        }
        
        self.listen_button = tk.Button(
            button_frame, text="🎤 Start Listening",
            command=self.toggle_listening,
            bg='#2ECC71', fg='white',
            activebackground='#27AE60',
            activeforeground='white',
            **button_style
        )
        self.listen_button.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, text="❓ Help",
            command=self.show_help,
            bg='#3498DB', fg='white',
            activebackground='#2980B9',
            activeforeground='white',
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame, text="🚪 Exit",
            command=self.exit_app,
            bg='#E74C3C', fg='white',
            activebackground='#C0392B',
            activeforeground='white',
            **button_style
        ).pack(side=tk.LEFT, padx=5)
        
        # Initialize welcome message
        self.add_assistant_message("Hello! I'm your voice assistant. Click 'Start Listening' to begin!")
        
    def add_user_message(self, message):
        """Add a user message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\n{timestamp} 👤 You: {message}\n")
        self.chat_display.see(tk.END)
        
    def add_assistant_message(self, message):
        """Add an assistant message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\n{timestamp} 🤖 Assistant: {message}\n")
        self.chat_display.see(tk.END)
        
    def update_status(self, status, color='#3498DB'):
        """Update the status label"""
        self.status_label.config(text=status, fg=color)
        
    def toggle_listening(self):
        """Toggle listening state"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening = True
            self.listen_button.config(text="🎤 Start Listening", bg='#2ECC71')
            self.update_status("Stopped listening", '#E74C3C')
            
    def process_voice_input(self):
        """Process voice input in a loop"""
        while not self.stop_listening:
            command = self.assistant.listen()
            if command:
                self.add_user_message(command)
                self.root.update()
                
                # Process the command
                result = self.assistant.process_command(command)
                if result is False:  # Exit command
                    self.stop_listening = True
                    self.is_listening = False
                    self.listen_button.config(text="🎤 Start Listening", bg='#2ECC71')
                    self.update_status("Ready to help!", '#3498DB')
                    break
        
        self.is_listening = False
        
    def start_listening(self):
        """Start listening for voice input"""
        self.is_listening = True
        self.stop_listening = False
        self.listen_button.config(text="⏹ Stop Listening", bg='#E74C3C')
        self.update_status("Listening...", '#2ECC71')
        
        # Start listening in a separate thread
        threading.Thread(target=self.process_voice_input, daemon=True).start()
        
    def show_help(self):
        """Show help information"""
        help_text = """
🎯 Here's what you can ask me to do:

⏰ Time and Date:
   Say "what time is it" or "what's the date"
   
🔍 Wikipedia Search:
   Say "search for [topic]" or "tell me about [topic]"
   
🌐 Open Websites:
   Say "open [website]" (e.g., "open youtube")
   
🎵 Music:
   Say "play music" to open Spotify
   
😄 Fun:
   Say "tell me a joke" for some humor
   
👋 Exit:
   Say "goodbye" or "exit" to quit
"""
        self.add_assistant_message(help_text)
        
    def exit_app(self):
        """Exit the application"""
        self.stop_listening = True
        self.root.after(500, self.root.destroy)  # Give time for threads to clean up
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    app = VoiceAssistantGUI()
    app.run()

if __name__ == "__main__":
    main()
