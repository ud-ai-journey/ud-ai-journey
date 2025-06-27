# prompt_builder.py
from moods import get_mood_details

def build_personalized_prompt(mood_key, duration, custom_topic=None, user_profile=None):
    """
    Builds a personalized prompt for the AI based on mood, duration, and user preferences.
    
    Args:
        mood_key (str): The mood key for the content
        duration (int): Duration in minutes
        custom_topic (str, optional): Custom topic if mood is 'custom'
        user_profile (UserProfile, optional): User profile containing preferences
        
    Returns:
        str: A personalized prompt for the AI
    """
    from user_profile import get_user_profile
    
    # Get user profile if not provided
    if user_profile is None:
        user_profile = get_user_profile()
    
    # Get mood details
    mood_details = get_mood_details(mood_key)
    
    # Base mood instructions
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
    
    # Start building the prompt with the base instruction
    prompt_parts = [instruction]
    
    # Add user preferences if available
    if user_profile and user_profile.is_profile_initialized():
        preferences = user_profile.get_all_preferences()
        
        # Add style preferences for this specific mood
        if f"style_positive_{mood_key}" in preferences:
            prompt_parts.append(f"Note: The user has enjoyed {mood_key} content in the past. "
                              f"Focus on what has worked well before.")
        
        # Add content style preference if available
        if "content_style" in preferences:
            prompt_parts.append(f"The user generally prefers content that is {preferences['content_style']}.")
        
        # Add any specific mood style descriptions
        mood_style = preferences.get(f"{mood_key}_style_description")
        if mood_style:
            prompt_parts.append(f"User feedback: {mood_style}")
        
        # Add time-specific preferences if available
        if "time_specific_style_preference" in preferences and "suggested_mood_for_time" in preferences:
            if preferences["suggested_mood_for_time"] == mood_key:
                prompt_parts.append(f"Note: {preferences['time_specific_style_preference']} "
                                  "This is a good time for this type of content.")
    
    # Add mood-specific guidance
    mood_guidance = {
        "learn": [
            "Include 1-2 key concepts with clear examples.",
            "Explain terms that might be unfamiliar to a general audience.",
            "End with a key takeaway or practical application."
        ],
        "reflect": [
            "Pose thoughtful, open-ended questions.",
            "Encourage self-exploration and mindfulness.",
            "Keep a calm and introspective tone."
        ],
        "story": [
            "Create a clear narrative with a beginning, middle, and end.",
            "Include descriptive details to set the scene.",
            "Develop characters or concepts that the user can connect with."
        ],
        "humor": [
            "Keep the tone light and entertaining.",
            "Use wordplay or situational humor when appropriate.",
            "Avoid offensive or controversial topics."
        ],
        "surprise": [
            "Include an unexpected twist or interesting fact.",
            "Challenge common assumptions.",
            "Spark curiosity with intriguing information."
        ]
    }
    
    # Add mood-specific guidance
    if mood_key in mood_guidance and mood_key != 'custom':
        prompt_parts.append("\nGuidelines for this mood:")
        prompt_parts.extend([f"- {item}" for item in mood_guidance[mood_key]])
    
    # Add duration-specific guidance
    prompt_parts.append("\nDuration guidance:")
    if duration <= 2:
        prompt_parts.extend([
            "- Keep it extremely brief - just one or two key points.",
            "- Focus on the most important aspect.",
            "- Be direct and to the point."
        ])
    elif duration <= 5:
        prompt_parts.extend([
            "- Be concise but complete - aim for about 1-2 focused paragraphs.",
            "- Include a clear introduction and conclusion.",
            "- Focus on 2-3 key points.",
            "- Use clear, simple language."
        ])
    elif duration <= 10:
        prompt_parts.extend([
            "- Provide a complete but focused piece - aim for about 3-5 paragraphs.",
            "- Include 3-4 key aspects of the topic.",
            "- Each paragraph should have a clear focus.",
            "- Use transitions to connect ideas smoothly."
        ])
    else:
        num_segments = max(2, duration // 10)
        prompt_parts.extend([
            f"- Create a comprehensive experience that can be naturally broken into {num_segments} segments.",
            "- Each segment should have its own mini-conclusion.",
            "- Focus on 4-5 key aspects.",
            "- Include natural pauses and transitions between segments.",
            "- Build toward a satisfying conclusion that ties everything together."
        ])
    
    # Add general guidance
    prompt_parts.extend([
        "\nGeneral guidelines:",
        f"- The total speaking time should be approximately {duration} minutes.",
        "- Speak naturally and conversationally.",
        "- Don't mention that you're an AI or assistant.",
        "- Tailor the response to align with the user's learned preferences.",
        "- Include natural pauses and transitions for walking.",
        "- Focus on delivering value without exceeding the time limit.",
        "- Maintain a clear, straightforward structure.",
        "- Use a friendly and engaging tone.",
        "- Keep paragraphs short and focused.",
        "- Use examples and analogies to explain complex ideas.",
        "- End with a clear conclusion or call to reflection."
    ])
    
    # Combine all parts into the final prompt
    final_prompt = "\n".join(prompt_parts)
    
    return final_prompt