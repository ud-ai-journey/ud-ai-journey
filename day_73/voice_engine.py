# voice_engine.py
import pyttsx3
import os
import time
from config import TTS_VOICE_ID, TTS_RATE, TTS_VOLUME, TTS_ENABLED

# Initialize TTS engine only if enabled in config
tts_engine = None  # Initialize as None first

def init_tts_engine():
    """Initialize the TTS engine with configured settings."""
    if not TTS_ENABLED:
        print("TTS feature is disabled in config.")
        return None

    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()
        
        # Apply configured voice ID if specified
        if TTS_VOICE_ID:
            try:
                engine.setProperty('voice', TTS_VOICE_ID)
            except Exception as voice_set_error:
                print(f"Warning: Could not set TTS voice ID: {voice_set_error}")
        
        # Apply configured rate if available
        try:
            engine.setProperty('rate', TTS_RATE)
        except (Exception, NameError) as rate_set_error:
            print(f"Warning: Could not set TTS rate: {rate_set_error}")
        
        # Apply configured volume if available
        try:
            engine.setProperty('volume', TTS_VOLUME)
        except (Exception, NameError) as vol_set_error:
            print(f"Warning: Could not set TTS volume: {vol_set_error}")
        
        return engine
            
    except Exception as init_error:
        print(f"Error initializing TTS engine: {init_error}")
        return None

# Initialize the TTS engine only once at module level
tts_engine = init_tts_engine()

# Ensure the audio directory exists
AUDIO_DIR = "audio"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

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
        print(f"Speaking content with length: {len(text)} characters")
        print(f"First 50 chars: {text[:50]}")
        
        # Ensure the engine is ready
        if not tts_engine.isBusy():
            # Clear any pending speech
            tts_engine.stop()
            tts_engine.endLoop()
            
            # Start new speaking session
            tts_engine.startLoop(False)
            tts_engine.say(text)
            
            # Run the speaking loop
            tts_engine.run()
            print("Finished speaking.")
            return True
        else:
            print("TTS engine is busy. Please wait.")
            return False
            
    except Exception as e:
        print(f"Error during pyttsx3 speech playback: {e}")
        print("Attempting to recover TTS engine...")
        try:
            # Try to fully reset the engine
            tts_engine.stop()
            tts_engine.endLoop()
            tts_engine = None
            tts_engine = init_tts_engine()
            print("TTS engine recovered.")
        except Exception as recover_error:
            print(f"Failed to recover TTS engine: {recover_error}")
        return False

def get_system_voices():
    """
    Retrieves a list of available system voices from pyttsx3.
    Returns a list of voice properties (dict per voice) or None if TTS is unavailable/no voices found.
    """
    try:
        # Initialize a temporary engine just for listing voices
        temp_engine = pyttsx3.init()
        voices = temp_engine.getProperty('voices')
        
        if voices:
            # Format voices for display
            voice_list = []
            for i, voice in enumerate(voices):
                voice_info = {
                    "Index": i,
                    "ID": voice.id,
                    "Name": voice.name,
                    "Languages": voice.languages,
                    "Gender": getattr(voice, 'gender', 'Unknown'),
                    "Age": getattr(voice, 'age', 'Unknown')
                }
                voice_list.append(voice_info)
            
            # Properly clean up the temporary engine
            temp_engine.stop()
            del temp_engine
            return voice_list
        else:
            print("No system voices found.")
            return []
    except Exception as e:
        print(f"Error listing system voices: {e}")
        return None

# Note: A function to save to file reliably with pyttsx3 across platforms is tricky.
# If file saving is a must-have, gTTS might be a better choice.
# For now, let's focus on direct speech playback.