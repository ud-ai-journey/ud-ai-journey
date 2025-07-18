import requests
import os

def generate_cohesive_story(memories, tone="Nostalgic"):
    """
    Generate a beautiful, cohesive story using Groq's LLM API based on user memories and selected tone.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it in your environment or .env file.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    prompt = (
        f"You are a masterful storyteller. Given the following personal memories, craft a single, beautiful, emotional, and cohesive story that weaves them all together. "
        f"Make the story {tone.lower()} in style. "
        "Make it suitable for sharing with friends and family, and keep it under 300 words.\n\n"
        f"Memories: {memories}\n\nStory:"
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a masterful, emotional storyteller."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 600,
        "temperature": 0.85
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    story = response.json()["choices"][0]["message"]["content"].strip()
    return story

def generate_title(memories):
    """
    Generate a beautiful, short, poetic title for the story based on the user's memories using Groq's LLM API.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it in your environment or .env file.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    prompt = (
        "Given these personal memories, generate a beautiful, short, poetic title (max 8 words) for a story that weaves them together.\n\n"
        f"Memories: {memories}\n\nTitle:"
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a poetic title generator."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 32,
        "temperature": 0.9
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    title = response.json()["choices"][0]["message"]["content"].strip().replace('"', '')
    return title

def generate_social_captions(memories, story, title):
    """
    Generate social captions for Instagram, LinkedIn, and X using Groq's LLM API.
    """
    import requests
    import os
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set. Please set it in your environment or .env file.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    prompt = (
        f"Given the following memories, story, and title, generate:\n"
        f"1. An Instagram caption (emotional, hashtag-rich, max 40 words)\n"
        f"2. A LinkedIn post (professional, reflective, max 60 words)\n"
        f"3. An X tweet (short, punchy, max 30 words)\n\n"
        f"Memories: {memories}\nTitle: {title}\nStory: {story}\n\n"
        "Format your response as:\nInstagram: ...\nLinkedIn: ...\nX: ..."
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a social media copywriter."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.9
    }
    response = requests.post(url, headers=headers, json=data, timeout=30)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()
    print("SOCIAL CAPTIONS RAW:", content)
    captions = {"instagram": "", "linkedin": "", "x": ""}
    for line in content.splitlines():
        if line.lower().startswith("instagram:"):
            captions["instagram"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("linkedin:"):
            captions["linkedin"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("x:"):
            captions["x"] = line.split(":", 1)[1].strip()
    # Fallbacks if LLM output is empty or not in expected format
    if not captions["instagram"]:
        captions["instagram"] = "Share your story and memories on Instagram! #MemoryLane"
    if not captions["linkedin"]:
        captions["linkedin"] = "Reflecting on beautiful moments and stories. #MemoryLane"
    if not captions["x"]:
        captions["x"] = "A special memory, a special story. #MemoryLane"
    return captions 