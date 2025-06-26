# voice_engine.py
import pyttsx3
import os
import time

# Ensure the audio directory exists
AUDIO_DIR = "audio"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# --- Initialize pyttsx3 Engine ---
try:
    # Initialize the TTS engine
    tts_engine = pyttsx3.init()

    # --- Voice Configuration (Optional: Customize voice properties) ---
    # Get available voices
    voices = tts_engine.getProperty('voices')
    
    # Set default voice (e.g., use the first available female voice if possible, else the first voice)
    # You might need to experiment to find voices that sound good on your system.
    # Common voice properties: 'id', 'name', 'languages', 'gender', 'age'
    
    # Example: Try to find a female voice
    preferred_voice_id = None
    for voice in voices:
        # Voice properties can vary wildly based on OS and installed voices.
        # This is a basic attempt; robust voice selection can be complex.
        if 'Zira' in voice.name or 'Helena' in voice.name or 'Hazel' in voice.name or 'en-US-Jessa' in voice.id or 'Female' in voice.name: # Example names/ids
             preferred_voice_id = voice.id
             break # Found one, use it
    
    # If no preferred voice found, use the first one available
    if not preferred_voice_id and voices:
        preferred_voice_id = voices[0].id # Fallback to the system's default voice
        
    if preferred_voice_id:
        tts_engine.setProperty('voice', preferred_voice_id)
        print(f"Using TTS voice: {tts_engine.getProperty('voice')}") # Print the ID of the voice being used
    else:
        print("Warning: Could not find or set a preferred TTS voice. Using system default.")

    # Set properties like rate (speed) and volume (optional)
    tts_engine.setProperty('rate', 175)  # Speed percentage (normal is 200) - adjust as needed
    # tts_engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)

except Exception as e:
    print(f"Error initializing pyttsx3 TTS engine: {e}")
    print("Voice output will be unavailable.")
    tts_engine = None

def text_to_speech_pyttsx3(text, output_filename="output.wav"):
    """
    Converts text to speech using pyttsx3 and saves it to a file.
    Note: pyttsx3 primarily speaks directly, saving requires specific driver support.
          Saving to file might not work reliably across all systems/drivers.
          We'll focus on speaking directly for simplicity first.
    
    Args:
        text (str): The text to convert to speech.
        output_filename (str, optional): Filename hint (saving is complex with pyttsx3).
                                         Defaults to "output.wav".
                                         
    Returns:
        bool: True if speaking started successfully, False otherwise.
    """
    if not tts_engine:
        print("TTS engine not initialized. Cannot convert text to speech.")
        return False

    if not text:
        print("No text provided for speech synthesis.")
        return False

    # pyttsx3's save_to_file method can be inconsistent.
    # For reliable file saving across platforms, gTTS or ElevenLabs are better.
    # For this phase, we'll primarily focus on speaking directly.
    # If saving is critical, we might need to explore platform-specific methods or a different library.
    
    # Let's try speaking directly first
    try:
        print("Speaking the content aloud...")
        tts_engine.say(text)
        tts_engine.runAndWait() # Blocks until speaking is finished
        tts_engine.stop() # Stop the engine after speaking
        print("Finished speaking.")
        return True
    except Exception as e:
        print(f"Error during pyttsx3 speech playback: {e}")
        return False

# Note: A function to save to file reliably with pyttsx3 across platforms is tricky.
# If file saving is a must-have, gTTS might be a better choice.
# For now, let's focus on direct speech playback.