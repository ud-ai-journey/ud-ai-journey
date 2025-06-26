# config.py
import os
from dotenv import load_dotenv
import sys 

# Load environment variables from .env file
load_dotenv()

# --- AI Configuration ---
# Use Ollama host from env var or default
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434") 

# --- LLM Model Configuration ---
# Allow overriding the default LLM model via environment variable
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "phi3:mini") 

# --- Voice Configuration ---
# Flag to enable/disable TTS feature based on environment variable
TTS_ENABLED = os.getenv("TTS_ENABLED", "true").lower() == "true" 
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
    print(f"Using LLM Model: {DEFAULT_LLM_MODEL}")
    if TTS_ENABLED:
        # Assumes pyttsx3 is the available TTS if TTS_ENABLED is true and ElevenLabs isn't configured.
        # A more robust check would explicitly test TTS availability here.
        print("Using pyttsx3 for Text-to-Speech (offline, system voices).")
    else:
        print("Text-to-Speech feature is disabled or unavailable.")