import threading
import time
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline

# Initialize emotion classifier (using a lightweight model)
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

class VoiceifyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voiceify Live Plus (Simplified)")
        self.root.geometry("500x300")

        self.label = tk.Label(root, text="Voiceify Live Plus: Day 38 (Simplified)", font=("Arial", 12))
        self.label.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD, font=("Arial", 10))
        self.output_text.pack(pady=5)
        self.output_text.insert(tk.END, "Click 'Start Listening' to begin.\n")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        self.start_button = tk.Button(self.button_frame, text="Start Listening", command=self.start_listening, font=("Arial", 10))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop Listening", command=self.stop_listening, state=tk.DISABLED, font=("Arial", 10))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.stop_event = threading.Event()
        self.listening_thread = None

    def log_to_gui(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()

    def start_listening(self):
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.log_to_gui("Adjusting for ambient noise... Please wait.")
        self.listening_thread = threading.Thread(target=self.continuous_listening)
        self.listening_thread.start()

    def stop_listening(self):
        self.stop_event.set()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log_to_gui("Listening stopped.")

    def continuous_listening(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            self.log_to_gui("🎙️ Speak now...")

            while not self.stop_event.is_set():
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    self.log_to_gui("🎙️ Processing...")
                    text = recognizer.recognize_google(audio)
                    self.log_to_gui(f"Transcribed: {text}")

                    # Basic emotion detection
                    emotion_data = classifier(text)[0]
                    emotion = emotion_data['label'].upper()
                    score = emotion_data['score']
                    self.log_to_gui(f"Emotion: {emotion} ({score:.2f})")
                except sr.WaitTimeoutError:
                    self.log_to_gui("No speech detected within 5 seconds.")
                except sr.UnknownValueError:
                    self.log_to_gui("Couldn’t understand the audio.")
                except sr.RequestError as e:
                    self.log_to_gui(f"Transcription error: {e}")
                    break
                except Exception as e:
                    self.log_to_gui(f"Error: {e}")
                    break
                time.sleep(0.1)

def main():
    print("🎙️ Voiceify Live Plus: Day 38 Simplified")
    root = tk.Tk()
    app = VoiceifyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()