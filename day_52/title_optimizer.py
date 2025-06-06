# Day 53: YouTube Title Optimizer - Logic for AI Optimization
# Uses Gemini API to generate optimized YouTube titles.

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file!")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)

def optimize_title(original_title, description, category):
    """
    Optimize a YouTube video title using Gemini API.
    Args:
        original_title (str): The original video title.
        description (str): The video description.
        category (str): The content category (e.g., Tech, Vlog).
    Returns:
        tuple: (improved_title, [alternate_titles], reason) or None if failed.
    """
    # Craft the prompt
    prompt = f"""
You are a world-class YouTube title coach with expertise in SEO and viral content creation. Rewrite the following title to make it more clickable, emotionally engaging, and SEO-optimized for the {category} category.

Original Title: "{original_title}"
Description: "{description}"

Return:
1. **Improved Title:** [Your improved title here (keep it under 70 characters for SEO)]
2. **Alternate Titles:**
   * [Alternate title 1 (under 70 characters)]
   * [Alternate title 2 (under 70 characters)]
   * [Alternate title 3 (under 70 characters)]
3. **Reason:** [1-2 sentences explaining why the new title is better]
"""

    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 150,
                "temperature": 0.7,
            }
        )

        # Parse the response
        result_text = response.text.strip()
        lines = result_text.split("\n")

        # Extract improved title, alternates, and reason
        improved_title = None
        alternates = []
        reason = ""

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("1. **Improved Title:**"):
                improved_title = line.replace("1. **Improved Title:**", "").strip()
            elif line.startswith("2. **Alternate Titles:**"):
                i += 1  # Move to the first bullet
                while i < len(lines) and lines[i].strip().startswith("*"):
                    alt_title = lines[i].strip().replace("*", "").strip()
                    if alt_title:
                        alternates.append(alt_title)
                    i += 1
                continue  # Skip increment since we already moved i
            elif line.startswith("3. **Reason:**"):
                reason = line.replace("3. **Reason:**", "").strip()
            i += 1

        if improved_title and len(alternates) == 3 and reason:
            return improved_title, alternates, reason
        else:
            print("❌ Parsing failed: Response format incorrect.")
            print("Response text:", result_text)
            return None

    except Exception as e:
        print(f"❌ Error calling Gemini API: {str(e)}")
        return None

# Example mock response (for testing without API key)
if __name__ == "__main__":
    # Mock input
    title = "My First Vlog in Paris"
    desc = "Join me on my first vlog as I explore the beautiful city of Paris!"
    cat = "Vlog"

    # Mock result (since I can't call the API directly)
    mock_result = (
        "🌟 My First Paris Vlog: Epic Adventures Await!",
        [
            "Paris Vlog #1: Unforgettable Moments! 🇫🇷",
            "First Time in Paris: Vlog You Can’t Miss! 🎥",
            "My Paris Journey Begins: Vlog 1 is Here! ✨"
        ],
        "The new title uses emojis and power words like 'Epic' and 'Await' to grab attention while keeping it SEO-friendly."
    )
    print("Mock Optimized Title:", mock_result[0])
    print("Mock Alternates:", mock_result[1])
    print("Mock Reason:", mock_result[2])