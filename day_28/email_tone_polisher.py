import os
from transformers import pipeline
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Initialize emotion detection pipeline
tone_detector = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",  # Better tone detection
    top_k=None
)

# Initialize text generation pipeline with T5-base
email_rewriter = pipeline(
    "text2text-generation",
    model="t5-base", 
    max_length=100,
    num_beams=4,
)

TONE_LABELS = {
    "anger": "Harsh",
    "disappointment": "Disappointed",
    "neutral": "Neutral",
    "surprise": "Surprised",
    "approval": "Positive",
    "joy": "Friendly",
    "sadness": "Sad",
    "confusion": "Confused",
}

def detect_tone(text):
    result = tone_detector(text)
    top_emotion = max(result[0], key=lambda x: x['score'])
    emotion_label = top_emotion['label']
    confidence = top_emotion['score']
    tone = TONE_LABELS.get(emotion_label, "Neutral")
    return tone, emotion_label, confidence

def generate_polished_email(original_text, tone_style):
    # Simplified prompt for T5-base
    prompt = (
        f"Paraphrase this to a {tone_style.lower()} and professional email: '{original_text}'. "
        f"Format: Subject: [Subject]\nDear [Recipient],\n[Body]\nBest regards,\n[Your Name]"
    )
    try:
        result = email_rewriter(prompt)[0]['generated_text'].strip()
        print(Fore.BLUE + f"Debug: Raw model output: {result}")
        # Post-process to ensure valid output
        if (
            "Subject:" in result
            and "Dear [Recipient]," in result
            and "Best regards," in result
            and original_text not in result
            and "Paraphrase" not in result
        ):
            return result
        else:
            print(Fore.YELLOW + "Warning: Model output invalid, using fallback response.")
            if tone_style.lower() == "surprised":
                return (
                    f"Subject: Inquiry About Your Delay\n\n"
                    f"Dear [Recipient],\n\n"
                    f"I was surprised to notice your delay today. Could you kindly provide an update on your availability? "
                    f"Thank you for your prompt response.\n\n"
                    f"Best regards,\n[Your Name]"
                )
            elif tone_style.lower() == "harsh":
                return (
                    f"Subject: Urgent Request\n\n"
                    f"Dear [Recipient],\n\n"
                    f"I noticed a delay in your response. Please provide an immediate update. Thank you.\n\n"
                    f"Best regards,\n[Your Name]"
                )
            else:
                return (
                    f"Subject: Request for Update\n\n"
                    f"Dear [Recipient],\n\n"
                    f"I hope you’re well. I noticed a delay and would appreciate an update on your availability. "
                    f"Thank you for your time.\n\n"
                    f"Best regards,\n[Your Name]"
                )
    except Exception as e:
        print(Fore.RED + f"Error generating response: {e}")
        return (
            f"Subject: Request for Update\n\n"
            f"Dear [Recipient],\n\n"
            f"I hope you’re well. I noticed a delay and would appreciate an update on your availability. "
            f"Thank you for your time.\n\n"
            f"Best regards,\n[Your Name]"
        )

def main():
    print(Fore.CYAN + "📝 Welcome to Email Tone Polisher!")
    while True:
        email_input = input(Fore.YELLOW + "\nEnter your raw email:\n")
        if not email_input.strip():
            print(Fore.RED + "Please enter some text.")
            continue

        # Detect tone
        tone, emotion_label, confidence = detect_tone(email_input)
        print(Fore.MAGENTA + f"\n🕵️‍♂️ Detected Tone: {tone} ({emotion_label}, confidence: {confidence:.2f})")
        print(Fore.BLUE + "💡 Suggestion: Consider rephrasing to sound more professional and appropriate.")

        # Generate polished version
        polished_email = generate_polished_email(email_input, tone)
        print(Fore.GREEN + f"\n🔧 Rewritten Email ({tone}):\n{polished_email}")

        # Ask for tone preference
        change_tone = input(Fore.CYAN + "\nWould you like to try a different tone? (y/n): ").lower()
        if change_tone == 'y':
            print("Choose desired tone: [Friendly / Assertive / Neutral / Professional / Polite]")
            desired_tone = input(Fore.YELLOW + "Your choice: ").strip()
            # Generate again with user-specified tone
            polished_email = generate_polished_email(email_input, desired_tone)
            print(Fore.GREEN + f"\n🔧 Rewritten Email ({desired_tone.capitalize()}):\n{polished_email}")

        # Option to process another email or exit
        again = input(Fore.CYAN + "\nWould you like to process another email? (y/n): ").lower()
        if again != 'y':
            print(Fore.MAGENTA + "Goodbye! Keep your emails impactful.")
            break

if __name__ == "__main__":
    main()