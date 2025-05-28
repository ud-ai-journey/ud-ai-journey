# Day 43: Emoji Translator (Updated with More Emojis)
# Converts words into emojis, loops until user types "exit".

def translate_to_emoji(sentence, emoji_dict):
    """
    Replace words in the sentence with emojis based on the emoji dictionary.
    """
    words = sentence.split()
    translated = []
    for word in words:
        # Remove punctuation for matching, but preserve it in the output
        clean_word = word.strip(".,!?").lower()
        if clean_word in emoji_dict:
            # Reattach punctuation to the emoji
            punctuation = word[len(clean_word):]
            translated.append(emoji_dict[clean_word] + punctuation)
        else:
            translated.append(word)
    return " ".join(translated)

def main():
    print("✨🌟 Day 43: Emoji Translator 🌟✨")
    print("📝 Enter a sentence to translate into emojis (type 'exit' to quit):")

    # Expanded emoji dictionary with more emotions and concepts
    emoji_dict = {
        "happy": "😊",
        "sad": "😢",
        "love": "❤️",
        "wow": "😲",
        "angry": "😡",
        "laugh": "😂",
        "cry": "😭",
        "cool": "😎",
        "party": "🥳",
        "tired": "😴",
        "scared": "😱",
        "think": "🤔",
        "dance": "💃",
        "hungry": "🍔",
        "sun": "☀️",
        "rain": "🌧️",
        "star": "⭐"
    }

    while True:
        # Get user input with emoji prompt
        sentence = input("\n✍️ Your sentence: ").strip()

        # Check for exit condition
        if sentence.lower() == "exit":
            print("👋🌈 Goodbye!")
            break

        if not sentence:
            print("⚠️📢 Please enter a sentence!")
            continue

        # Translate the sentence
        result = translate_to_emoji(sentence, emoji_dict)
        print(f"🎉 Translated: {result}")

if __name__ == "__main__":
    main()

# Committed on 28th May,2025 after Shirdi Darshan