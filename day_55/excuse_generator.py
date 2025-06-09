# Day 55: AI-Powered Excuse Generator (Console App)
# Generates creative excuses using the Gemini API

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

def generate_excuse(context, tone):
    """
    Generate an excuse using the Gemini API.
    Args:
        context (str): The scenario needing an excuse (e.g., "late assignment").
        tone (str): The tone of the excuse (e.g., "funny", "professional").
    Returns:
        str: The generated excuse, or an error message if failed.
    """
    # Craft the prompt
    prompt = f"""
You are a creative writer specializing in crafting believable and natural excuses. Generate a {tone} excuse for the following scenario: {context}. The excuse should be short (1-2 sentences), creative, and sound natural for the given tone. Return only the excuse, no additional explanation.
"""

    try:
        # Initialize Gemini model (using gemini-1.5-flash for efficiency)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Generate content
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 50,
                "temperature": 0.9,  # Higher temperature for creative responses
            }
        )

        # Return the generated excuse
        return response.text.strip()

    except Exception as e:
        return f"❌ Error generating excuse: {str(e)}"

def main():
    # Print welcome message
    print("🤖 AI-Powered Excuse Generator 🤖")
    print("Generate creative excuses in seconds!")
    print("-" * 40)

    # Get user input
    context = input("Why do you need an excuse for? (e.g., late assignment, missing gym): ").strip()
    tone = input("What kind of excuse do you want? (funny, emotional, serious, professional): ").strip().lower()

    # Validate input
    if not context or not tone:
        print("❌ Please provide both a context and a tone!")
        return

    # Generate the excuse
    print("\nGenerating your excuse... 🤔")
    excuse = generate_excuse(context, tone)

    # Display the excuse
    print("\nHere's your excuse: 🤖")
    print(excuse)

if __name__ == "__main__":
    main()