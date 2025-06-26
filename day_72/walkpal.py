# walkpal.py

import time
import sys
import os 
from datetime import datetime 

# --- Imports ---
from moods import get_mood_details, VALID_MOODS
from config import check_config, TTS_ENABLED, DEFAULT_LLM_MODEL
# AI engine updated to handle conversation history and return assistant message
try:
    from ai_engine import generate_ai_content 
except ImportError:
    print("Error importing ai_engine. Make sure it's correctly set up.")
    sys.exit(1)

# TTS availability check (assuming pyttsx3 is the default if TTS_ENABLED is True)
try:
    from voice_engine import text_to_speech_pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    print("pyttsx3 library not found. Voice output will be unavailable.")
    TTS_AVAILABLE = False
except Exception as e: 
    print(f"Error initializing TTS: {e}. Voice output will be unavailable.")
    TTS_AVAILABLE = False

# Data and Pattern Analysis imports
from data_manager import log_walk_session, save_feedback, load_walk_log 
from pattern_engine import suggest_mood_for_time, analyze_session_data, generate_insights
from user_profile import get_user_profile 
from prompt_builder import build_personalized_prompt 


# --- Constants and Global Variables ---
# Store analysis data globally after first load
analysis_data = None 


# Approximate words per minute for estimating content length
AVG_WORDS_PER_MINUTE = 150 

# --- Helper Functions ---
def estimate_speaking_time_minutes(text):
    """
    Estimates the speaking time of text in minutes based on word count and content type.
    
    Args:
        text (str): The text to estimate speaking time for
        
    Returns:
        float: Estimated speaking time in minutes (minimum 0.5 minutes)
    """
    if not text or not text.strip():
        return 0.5
        
    # Count words and characters
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    
    # Calculate words per minute (slower for complex content)
    wpm = 150  # Average speaking rate
    
    # Adjust WPM based on content complexity
    avg_word_length = char_count / max(1, word_count)
    if avg_word_length > 6:  # Longer words indicate more complex content
        wpm = max(100, wpm * 0.8)  # Slow down for complex content
    
    # Calculate base time
    base_time = word_count / wpm
    
    # Add time for pauses, punctuation, and line breaks
    pause_factors = text.count('.') * 0.1 + text.count('!') * 0.15 + text.count('?') * 0.15
    line_breaks = text.count('\n') * 0.1
    
    # Calculate total time with adjustments
    total_time = base_time + pause_factors + line_breaks
    
    # Ensure minimum duration
    return max(0.5, round(total_time, 1))  # At least 30 seconds, rounded to 1 decimal

def load_and_analyze_data_globally():
    """Loads walk log and performs analysis, updating the global analysis_data."""
    global analysis_data 
    print("\n=== Starting data load and analysis ===")
    try:
        print("Loading walk log...")
        log_data = load_walk_log()
        print(f"Loaded {len(log_data) if log_data else 0} log entries")
        
        print("Analyzing session data...")
        analysis_data = analyze_session_data(log_data)
        
        if analysis_data:
            print(f"Analysis complete. Total sessions: {analysis_data.get('total_sessions', 0)}")
            if 'mood_distribution' in analysis_data:
                print(f"Mood distribution: {analysis_data['mood_distribution']}")
        else:
            print("No analysis data returned")
            
        return analysis_data
    except Exception as e:
        print(f"ERROR in load_and_analyze_data_globally: {e}")
        import traceback
        traceback.print_exc()
        analysis_data = None 
        return None

def get_walk_preferences(suggested_mood_key=None):
    """
    Prompts user for walk duration, mood (using suggestion if available), and output mode.
    Supports both general moods and custom topics.
    Validates inputs and returns them.
    """
    # Get duration
    while True:
        print("\nHow long is your walk? (in minutes)")
        print("Quick select: 5 / 10 / 15 minutes")
        print("Or enter any whole number (e.g., 2, 7, 20, 45, etc.)")
        duration_input = input("\nEnter walk duration (minutes): ")
        try:
            duration = int(duration_input)
            if duration <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    # Get mood choice with suggestion
    print("\nWhat kind of vibe are you looking for on this walk?")
    print("Options: Learn Something New, Reflect & Reset, Storytime, Make Me Laugh, Surprise Me!")
    print("Or enter a custom topic (e.g., 'story of vijay mallya', 'ramayan', 'business tactics by tim cook', 'comedy')")
    mood_prompt = "Enter your mood choice [{}]: ".format(suggested_mood_key or "Make Me Laugh")
    mood_input = input(mood_prompt)
    
    # Validate mood
    if mood_input:
        mood_choice = mood_input.lower()
        # Check if it's a custom topic
        if mood_choice not in VALID_MOODS:
            mood_choice = "custom"
            custom_topic = mood_input
        else:
            custom_topic = None
    else:
        mood_choice = suggested_mood_key.lower() if suggested_mood_key else "humor"
        custom_topic = None

    # Final validation
    if mood_choice not in VALID_MOODS:
        print("\nInvalid mood choice. Using default: Make Me Laugh")
        mood_choice = "humor"
        custom_topic = None

    # Get output mode
    while True:
        mode_input = input("\nChoose output mode: (Text / Audio): ").lower()
        if mode_input in ["text", "audio"]:
            output_mode = mode_input
            break
        print("Please enter either 'text' or 'audio'.")

    return duration, mood_choice, output_mode, custom_topic

def get_and_save_feedback(last_log_id):
    """Prompts for feedback and saves it if provided, associated with the last logged session."""
    if last_log_id is None: return 

    feedback_score = None
    while True:
        feedback_input = input("\nHow was this session? (1-5 stars, or press Enter to skip): ").strip()
        if not feedback_input: 
            print("Skipping feedback.")
            break 
        try:
            score = int(feedback_input)
            if 1 <= score <= 5:
                feedback_score = score
                break 
            else:
                print("Invalid input. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number or press Enter to skip.")
            
    if feedback_score is not None:
        save_feedback(last_log_id, feedback_score)


# --- Function to get ONE content chunk ---
# This function's sole purpose is to call the AI engine.
def get_content_chunk(mood_key, duration, conversation_history, custom_topic=None):
    """
    Generates a single piece of AI content for the current turn with enhanced quality control.
    
    Args:
        mood_key (str): The chosen mood key.
        duration (int): The chosen duration.
        conversation_history (list): List of previous messages for context.
        custom_topic (str, optional): Specific topic if mood_key is 'custom'
        
    Returns:
        tuple: (generated_text_chunk, assistant_message) where assistant_message is the
               AI's response formatted for history, or (error_message, None) if generation fails.
    """
    try:
        # Validate inputs
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer")
        if mood_key == 'custom' and (not custom_topic or not isinstance(custom_topic, str)):
            raise ValueError("Custom topic must be provided as a string when mood_key is 'custom'")

        # Build personalized prompt
        full_personalized_prompt = build_personalized_prompt(mood_key, duration, custom_topic)

        # Generate content with retries
        max_retries = 3
        retry_delay = 2  # seconds
        for attempt in range(max_retries):
            try:
                # Generate content
                generated_text_chunk, assistant_message = generate_ai_content(full_personalized_prompt, conversation_history)
                
                # Basic quality check
                if not generated_text_chunk or generated_text_chunk.strip() == "":
                    raise ValueError("Generated content is empty")
                    
                # Clean up content
                cleaned_content = generated_text_chunk.strip()
                
                # Check for meta-content or self-reference (only check for obvious AI references)
                if 'walkpal' in cleaned_content.lower():
                    raise ValueError("Content contains meta-content or self-reference")
                
                # Check for reasonable length
                word_count = len(cleaned_content.split())
                max_words = duration * 150  # 150 words per minute max
                min_words = duration * 50   # 50 words per minute min
                
                if word_count > max_words:
                    # Truncate instead of failing
                    words = cleaned_content.split()[:max_words]
                    cleaned_content = ' '.join(words) + '...'
                elif word_count < min_words:
                    # Skip minimum length check for now to avoid false positives
                    pass
                    
                # Basic topic relevance check for custom topics
                if mood_key == 'custom' and custom_topic and len(custom_topic.split()) > 1:
                    topic_words = set(custom_topic.lower().split())
                    content_words = set(cleaned_content.lower().split())
                    if not any(word in content_words for word in topic_words):
                        # If no topic words found, just log a warning but don't fail
                        print("Warning: Content may not fully match the requested topic")
                        
                return cleaned_content, assistant_message
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise  # Re-raise on final attempt
                print(f"Content generation attempt {attempt + 1} failed: {e}")
                time.sleep(retry_delay)
                
    except Exception as e:
        error_msg = f"Error generating content: {str(e)}"
        print(error_msg)
        return error_msg, None


# --- Main Orchestration Function ---
def main():
    """
    Orchestrates the entire WalkPal application flow.
    Handles configuration, profile loading, user interaction, iterative content generation,
    logging, feedback, and TTS output.
    """
    try:
        check_config() # Validate configurations at the start
    except Exception as e: 
        print(f"Configuration Error: {e}")
        sys.exit(1) 

    # --- Initialize Profile and Load Data ---
    global user_profile, analysis_data 
    # Get/create the singleton profile instance. This also loads and analyzes data internally.
    user_profile = get_user_profile() 
    # Get analysis results from the profile after initialization
    analysis_data = user_profile.analysis_data 

    # --- Display Insights ---
    # Generate and display insights if profile is initialized and analysis data is ready
    if user_profile and user_profile.is_profile_initialized() and analysis_data:
         insights = generate_insights(analysis_data)
         print("\n--- Your Walk History Insights ---")
         print(insights)
         print("----------------------------------")


    suggested_mood_key = None 
    # Provide mood suggestions if profile is initialized and analysis data is ready
    if user_profile and user_profile.is_profile_initialized() and analysis_data:
        current_hour = datetime.now().hour
        suggested_mood_key = suggest_mood_for_time(current_hour, analysis_data)
        # The hint is now printed within get_walk_preferences if suggested_mood_key is not None

    # --- Get User Preferences ---
    # Pass the suggestion to get_walk_preferences so it can be used as a default
    duration, mood_choice, output_mode, custom_topic = get_walk_preferences(suggested_mood_key)
    
    # --- Calculate Chunking for Long Walks ---
    # For longer walks, break into smaller segments with natural breaks
    if duration <= 5:
        chunk_duration = duration
        num_chunks = 1
    elif duration <= 15:
        chunk_duration = min(5, duration)  # 5-minute chunks for medium walks
        num_chunks = max(1, (duration + chunk_duration - 1) // chunk_duration)  # Ceiling division
    else:
        # For very long walks, aim for 10-15 minute segments
        chunk_duration = min(15, max(10, duration // 3))
        num_chunks = max(1, (duration + chunk_duration - 1) // chunk_duration)

    print(f"\nPreparing {duration}-minute walk in {num_chunks} chunk{'s' if num_chunks > 1 else ''}...")

    # --- Interactive Content Generation Loop ---
    content_generated_so_far = ""  # Accumulates all generated text
    conversation_history = []  # Manages history for AI turns
    last_logged_session_id = None  # Tracks the ID for feedback
    total_estimated_time = 0  # Track total estimated speaking time
    
    print("\nStarting content generation...")

    # For story mode or custom topics, generate the entire content at once
    if mood_choice == 'story' or mood_choice == 'custom':
        print(f"\nGenerating complete content for {duration} minutes...")
        generated_text_chunk, assistant_message = get_content_chunk(mood_choice, duration, conversation_history, custom_topic)
        
        if not generated_text_chunk or generated_text_chunk.strip() == "":
            print("Error generating content. Stopping walk.")
            return last_logged_session_id
            
        # Update conversation history and content
        conversation_history.append(assistant_message)
        content_generated_so_far = generated_text_chunk
        total_estimated_time = estimate_speaking_time_minutes(generated_text_chunk)
        
        print(f"\n--- Complete Content Generated (~{total_estimated_time:.1f} min) ---")
        print(generated_text_chunk.strip())
        
    else:
        # For other modes, use chunked generation
        while total_estimated_time < duration:
            # Calculate target duration for this chunk
            if duration <= 5:
                target_chunk_duration = duration  # For short walks, generate all at once
            elif total_estimated_time < duration - 2:
                target_chunk_duration = min(5, duration - total_estimated_time)  # Generate up to 5 minutes at a time
            else:
                target_chunk_duration = duration - total_estimated_time  # Last chunk should match remaining time

            print(f"\nGenerating content chunk for ~{target_chunk_duration:.1f} minutes...")
            
            # Get new content chunk
            generated_text_chunk, assistant_message = get_content_chunk(mood_choice, target_chunk_duration, conversation_history)
            
            if not generated_text_chunk:
                print("Error generating content. Stopping walk.")
                return last_logged_session_id
                
            # Update conversation history with this chunk
            conversation_history.append(assistant_message)
            
            # Add to our cumulative content
            content_generated_so_far += generated_text_chunk + "\n\n"
            
            # Estimate speaking time for this chunk
            chunk_time = estimate_speaking_time_minutes(generated_text_chunk)
            total_estimated_time += chunk_time
            
            print(f"\n--- Chunk Generated (~{chunk_time:.1f} min) ---")
            print(generated_text_chunk.strip())
            
            # Check if we've reached or exceeded the target duration
            if total_estimated_time >= duration - 0.5:
                break
                
            # Ask user if they want to continue
            more_input = input("\nTotal content so far ~{:.1f}/{:.1f} min. Continue? (y/N): ".format(total_estimated_time, duration))
            if more_input.lower() not in ['y', 'yes']:
                print("\nStopping content generation as requested.")
                
                # Log the session before returning
                audio_was_used_for_session = output_mode == "audio" and TTS_AVAILABLE and bool(content_generated_so_far.strip())
                last_logged_session_id = log_walk_session(
                    duration, mood_choice, content_generated_so_far, audio_was_used_for_session
                )
                
                # Prompt for feedback
                get_and_save_feedback(last_logged_session_id)
                
                return last_logged_session_id
                
            # Play audio chunk if applicable and TTS is available
            if output_mode == "audio" and TTS_AVAILABLE:
                print("\nSpeaking chunk...")
                text_to_speech_pyttsx3(text=generated_text_chunk)
                print("Finished speaking.")

    print("\nContent generation finished.")
    print(f"\nTotal estimated speaking time: {total_estimated_time:.1f} minutes")
    
    # --- Log the session ---
    audio_was_used_for_session = output_mode == "audio" and TTS_AVAILABLE and bool(content_generated_so_far.strip())
    last_logged_session_id = log_walk_session(
        duration, mood_choice, content_generated_so_far, audio_was_used_for_session
    )
    
    # --- Output the final content ---
    print("\n" + "*" * 50)
    print(f" Walk Summary for your {duration}-minute walk")
    print("*" * 50)
    
    mood_display_name = get_mood_details(mood_choice)['name']
    print(f"\n--- Full WalkPal Content ({mood_display_name}) ---")
    print(content_generated_so_far.strip())
    
    # --- Play final audio if in audio mode ---
    if output_mode == "audio" and TTS_AVAILABLE and content_generated_so_far.strip():
        print("\nSpeaking final content...")
        text_to_speech_pyttsx3(text=content_generated_so_far)
        print("Finished speaking.")
    
    print("\n" + "-" * 50)
    print("Enjoy your walk!")
    print("-" * 50)

    # Prompt for feedback for the session using the ID logged from the first chunk
    get_and_save_feedback(last_logged_session_id)
    
    return last_logged_session_id  # Return the session ID for feedback if needed


# --- Main execution block ---
if __name__ == "__main__":
    main()