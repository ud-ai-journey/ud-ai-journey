# prompt_builder.py
from moods import get_mood_details

def build_personalized_prompt(mood_key, duration, custom_topic=None):
    """
    Builds a simple prompt for the AI based on mood and duration.
    """
    mood_details = get_mood_details(mood_key)
    
    # Simple mood instructions
    mood_map = {
        "learn": "Share an interesting lesson with examples",
        "reflect": "Provide thoughtful reflections",
        "story": "Tell an engaging story",
        "humor": "Share something funny",
        "surprise": "Share something surprising",
        "custom": f"Talk about {custom_topic}" if custom_topic else "Share something interesting"
    }
    
    # Get the base instruction
    instruction = mood_map.get(mood_key, mood_map["surprise"])
    
    # Add duration context
    instruction += f" that would take about {duration} minutes to read aloud."
    
    # For custom topics, add more context
    if mood_key == 'custom' and custom_topic:
        mood_details['name'] = f"Custom: {custom_topic}"
        instruction = f"Share interesting information about {custom_topic} that would take about {duration} minutes to read aloud."
    
    # Simple prompt
    prompt = f"""{instruction}

Speak naturally and conversationally. Don't mention that you're an AI or assistant."""
    
    # Add duration-specific guidance
    duration_guidance = []
    if duration <= 2:
        duration_guidance.append("Keep it extremely brief - just one or two key points.")
        duration_guidance.append("Focus on the most important aspect.")
    elif duration <= 5:
        duration_guidance.append("Be concise but complete - aim for about 1-2 focused paragraphs.")
        duration_guidance.append("Include a clear introduction and conclusion.")
        duration_guidance.append("Focus on 2-3 key points.")
    elif duration <= 10:
        duration_guidance.append("Provide a complete but focused piece - aim for about 3-5 paragraphs.")
        duration_guidance.append("Include 3-4 key aspects of the topic.")
        duration_guidance.append("Each paragraph should have a clear focus.")
    else:
        duration_guidance.append(f"Create a comprehensive experience that can be naturally broken into {max(2, duration // 10)} segments.")
        duration_guidance.append("Each segment should have its own mini-conclusion.")
        duration_guidance.append("Focus on 4-5 key aspects.")
    
    # Add general guidance
    duration_guidance.append(f"The total speaking time should be approximately {duration} minutes.")
    duration_guidance.append("Tailor the response to align with the user's learned preferences where possible.")
    duration_guidance.append("Include natural pauses and transitions for walking.")
    duration_guidance.append("Focus on delivering value without exceeding the time limit.")
    duration_guidance.append("Maintain a clear, straightforward structure.")
    
    # Combine all parts
    final_prompt = prompt + "\n\n" + "\n".join(duration_guidance)
    
    return final_prompt