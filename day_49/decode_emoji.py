import random
import unicodedata

def load_emoji_map():
    return {
        "🍎": "A", "🐝": "B", "🐱": "C", "🐶": "D", "🐘": "E",
        "🐸": "F", "🦒": "G", "🏠": "H", "🍦": "I", "🕹️": "J",
        "🎋": "K", "🦁": "L", "🌝": "M", "🎶": "N", "🐙": "O",
        "🥞": "P", "👸": "Q", "🤖": "R", "🐍": "S", "🌴": "T",
        "🦄": "U", "🎻": "V", "🌊": "W", "❌": "X", "🪀": "Y",
        "🦓": "Z"
    }

def split_emojis(message):
    """Split a string into individual emojis, handling multi-codepoint emojis."""
    emojis = []
    i = 0
    while i < len(message):
        char = message[i]
        # Check for surrogate pairs or multi-codepoint emojis
        if i + 1 < len(message) and unicodedata.category(message[i + 1]).startswith('M'):
            emojis.append(char + message[i + 1])
            i += 2
        else:
            emojis.append(char)
            i += 1
    return emojis

def decode_emoji(emoji_message, emoji_map):
    emojis = split_emojis(emoji_message)
    decoded = ""
    for emoji in emojis:
        decoded += emoji_map.get(emoji, "?")
    return decoded

def encode_message(text_message, emoji_map):
    reverse_map = {v: k for k, v in emoji_map.items()}
    encoded = ""
    for char in text_message.upper():
        encoded += reverse_map.get(char, char)
    return encoded

def guess_game(emoji_map):
    words = ["CAT", "DOG", "HOME", "SNAKE", "MUSIC"]
    score = 0
    rounds = 3
    
    print(f"\n🎮 Emoji Guessing Game! Guess the word for each emoji sequence ({rounds} rounds).")
    print("Hint: Enter a single word (e.g., CAT, not 'cat,apple,tree').")
    reverse_map = {v: k for k, v in emoji_map.items()}
    
    for round_num in range(1, rounds + 1):
        word = random.choice(words)
        emoji_word = "".join(reverse_map[char] for char in word)
        print(f"\nRound {round_num}/{rounds}: Decode this: {emoji_word}")
        guess = input("Your guess (one word): ").strip().upper()
        
        if "," in guess or " " in guess:
            print("🚨 Please enter a single word without commas or spaces.")
            print(f"❌ Nope! It was {word}.")
            continue
        
        if guess == word:
            print("✅ Correct! You're an emoji master!")
            score += 1
        else:
            print(f"❌ Nope! It was {word}.")
    
    print(f"\n🏆 Game Over! Score: {score}/{rounds}")
    if score == rounds:
        print("Emoji Mastermind! 🧠")
    elif score > 0:
        print("Nice decoding skills! Keep practicing! 😄")
    else:
        print("No worries, you'll crack the code next time! 🔐")
    return score

def main():
    print("🔐 Emoji Cipher Decoder & Encoder 😄")
    emoji_map = load_emoji_map()
    
    while True:
        print("\nChoose an option:")
        print("1. Decode an emoji message")
        print("2. Encode a text message")
        print("3. Play the emoji guessing game")
        print("4. Exit")
        
        choice = input("Enter 1-4: ").strip()
        
        try:
            if choice == "1":
                print("Enter emojis (e.g., 🐍🍎🐝 for SAB). Use Windows Key + . to open emoji picker.")
                emoji_message = input("Emoji message: ").strip()
                if not emoji_message:
                    print("🚨 Please enter at least one emoji.")
                    continue
                decoded = decode_emoji(emoji_message, emoji_map)
                if decoded == "?" * len(decoded):
                    print("🚨 No valid emojis found. Use emojis like 🐍🍎🐝 from the map.")
                else:
                    print("🔓 Decoded Message:", decoded)
            
            elif choice == "2":
                print("Enter a word or phrase (letters A-Z only, e.g., HELLO).")
                text_message = input("Text message: ").strip()
                if not text_message.replace(" ", "").isalpha():
                    print("🚨 Please use letters only (A-Z).")
                    continue
                encoded = encode_message(text_message, emoji_map)
                print("🔒 Encoded Message:", encoded)
            
            elif choice == "3":
                guess_game(emoji_map)
            
            elif choice == "4":
                print("👋 Thanks for playing! Stay cryptic!")
                break
            
            else:
                print("🚨 Invalid choice. Pick 1-4.")
        
        except Exception as e:
            print(f"🚨 Error: Invalid input. Try again.")

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\n🚨 Input interrupted. Exiting game.")