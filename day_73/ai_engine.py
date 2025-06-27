# ai_engine.py
import ollama 
import time
import sys
import os 

# --- Imports ---
from config import DEFAULT_LLM_MODEL, OLLAMA_HOST 
from prompts import SYSTEM_MESSAGE_BASE # Base system message remains essential

def clean_ai_output(text):
    """
    Simple cleanup of AI output.
    """
    if not text:
        return text
    
    # Just return the text as-is, but strip any extra whitespace
    return text.strip()

# --- Ollama Client Setup ---
# Ollama.chat works directly with the configured host. No explicit client instantiation needed usually.
# A basic check could be added here to ping Ollama, but let's rely on request errors for now.

def generate_ai_content(full_prompt, conversation_history=None):
    """
    Generates content using a local Ollama model based on a potentially multi-turn prompt.
    
    Args:
        full_prompt (str): The complete, pre-constructed prompt for the current turn (user message).
        conversation_history (list, optional): A list of previous messages ({'role': ..., 'content': ...})
                                             for multi-turn context. Defaults to None.
                                             
    Returns:
        str: The generated text content from the AI, or an error message.
    """
    
    model_to_use = DEFAULT_LLM_MODEL 
    
    print(f"\nSubmitting prompt to local model ({model_to_use})...")

    # --- Construct the messages list for Ollama API ---
    messages = []
    
    # Add a minimal system message to avoid meta-content
    messages.append({
        'role': 'system',
        'content': "You are a helpful assistant. Provide clear, concise responses without any meta-commentary."
    })
    
    # Add previous conversation history if provided. This is key for iterative generation.
    if conversation_history:
        messages.extend(conversation_history)
        
    # Add the current user prompt (which is the final personalized prompt for this turn).
    messages.append({
        'role': 'user',
        'content': full_prompt, 
    })

    try:
        # --- Call Ollama API ---
        response = ollama.chat(
            model=model_to_use,
            messages=messages, # Pass the complete list of messages
            options={'temperature': 0.7} # Can be tuned
        )
        
        generated_text = response['message']['content'].strip()
        
        # Clean up the generated text to remove any metadata or context
        cleaned_text = clean_ai_output(generated_text)
        
        print("Local AI generation successful.")
        # Return the generated text AND the updated conversation history
        return cleaned_text, {
            'role': 'assistant',
            'content': cleaned_text
        }

    # --- Error Handling for Ollama ---
    except ollama.ResponseError as e:
        print(f"Ollama API error: {e.error} (Status: {e.status_code})")
        if "model not found" in e.error.lower():
             return f"Error: The requested model '{model_to_use}' was not found. Ensure it's downloaded via Ollama (`ollama pull {model_to_use}`).", None
        return f"Sorry, there was an issue communicating with the local AI model: {e.error}. Please check Ollama logs.", None
    except Exception as e:
        print(f"An unexpected error occurred during local AI generation: {e}")
        if "Failed to connect to Ollama" in str(e):
             return f"Sorry, failed to connect to Ollama. Is Ollama running and '{model_to_use}' downloaded? Check: https://ollama.com/download", None
        return "Sorry, something went wrong while generating your content locally.", None