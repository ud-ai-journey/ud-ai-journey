from gtts import gTTS
import pyttsx3
import os

def text_to_speech(text, output_path):
    """
    Convert text to speech and save as mp3. Use gTTS for natural voice, fallback to pyttsx3 if offline.
    """
    try:
        tts = gTTS(text)
        tts.save(output_path)
    except Exception as e:
        # Fallback to pyttsx3 (offline, but more robotic)
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait() 