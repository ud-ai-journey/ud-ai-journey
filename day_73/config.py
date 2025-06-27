# config.py
import os
from dotenv import load_dotenv
import sys 
import os

# Load environment variables from .env file
load_dotenv()

# --- AI Configuration ---
# Use Ollama host from env var or default
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434") 

# --- LLM Model Configuration ---
# Allow overriding the default LLM model via environment variable
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "phi3:mini") 

# --- Language Configuration ---
# Default to English if not specified
DEFAULT_LANGUAGE = os.getenv("WALKPAL_LANG", "en")

# --- Voice Configuration ---
# Flag to enable/disable TTS feature based on environment variable
TTS_ENABLED = os.getenv("TTS_ENABLED", "true").lower() == "true" 
# Settings for pyttsx3
TTS_VOICE_ID = os.getenv("WALKPAL_TTS_VOICE_ID")  # Can be None initially

# Initialize with string values from environment
_TTS_RATE_STR = os.getenv("WALKPAL_TTS_RATE", "175")  # Default speaking rate
_TTS_VOLUME_STR = os.getenv("WALKPAL_TTS_VOLUME", "1.0")  # Default volume (0.0 to 1.0)

# Initialize with default values that will be updated in check_config()
TTS_RATE = 175
TTS_VOLUME = 1.0

# If TTS is enabled, we implicitly rely on pyttsx3 availability or other configured engines
# We don't need ElevenLabs specific keys here anymore if using pyttsx3

# --- Personalization Configuration ---
# Minimum number of walks required before insights/suggestions become active
MIN_WALKS_FOR_INSIGHTS = 3 
MIN_WALKS_FOR_PREDICTIONS = 5 
# How strongly to incorporate personalized suggestions into prompts (0.0 to 1.0)
# Higher value means stronger influence. Not directly used in current prompt builder but planned.
PERSONALIZATION_STRENGTH = 0.7 

def check_config():
    """Checks essential configuration and prints relevant settings."""
    global TTS_RATE, TTS_VOLUME  # Declare we're modifying the global variables
    
    print(f"Using LLM Model: {DEFAULT_LLM_MODEL}")
    print(f"Using Language: {DEFAULT_LANGUAGE}")
    
    # Process TTS rate
    try:
        TTS_RATE = int(_TTS_RATE_STR)
    except (ValueError, TypeError):
        print(f"Warning: Invalid value for WALKPAL_TTS_RATE '{_TTS_RATE_STR}'. Using default (175).")
        TTS_RATE = 175
    
    # Process TTS volume
    try:
        TTS_VOLUME = float(_TTS_VOLUME_STR)
        if not (0.0 <= TTS_VOLUME <= 1.0):
            print(f"Warning: WALKPAL_TTS_VOLUME '{_TTS_VOLUME_STR}' is outside valid range [0.0, 1.0]. Using default (1.0).")
            TTS_VOLUME = 1.0
    except (ValueError, TypeError):
        print(f"Warning: Invalid value for WALKPAL_TTS_VOLUME '{_TTS_VOLUME_STR}'. Using default (1.0).")
        TTS_VOLUME = 1.0
    
    # Print TTS configuration
    if TTS_ENABLED:
        print("Using pyttsx3 for Text-to-Speech (offline, system voices).")
        if TTS_VOICE_ID:
            print(f"  Configured Voice ID: {TTS_VOICE_ID}")
        else:
            print("  Using system default voice.")
        print(f"  Configured Rate: {TTS_RATE}")
        print(f"  Configured Volume: {TTS_VOLUME}")
    else:
        print("Text-to-Speech feature is disabled or unavailable.")