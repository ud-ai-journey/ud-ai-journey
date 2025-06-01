import random

print("Let's create a story!")

# Collect user inputs
name = input("What's the name of the main character? ").strip()
place = input("Where does the story take place? (e.g., a forest, a castle, a spaceship) ").strip()
magical_object = input("What's a magical object? (e.g., a wand, a crystal, a book) ").strip()
emotion = input("What's an emotion? (e.g., joy, fear, excitement) ").strip()
verb = input("What's a funny verb? (e.g., screamed, danced, vanished) ").strip()

# Ensure the number is a valid integer
while True:
    number = input("Pick a number: ").strip()
    try:
        number = int(number)
        break
    except ValueError:
        print("Please enter a valid integer.")

# Story templates with placeholders and emojis
templates = [
    "Once upon a time, in the mysterious land of {place} 🏰, there lived a person named {name}. "
    "One day, they found a magical {magical_object} ✨ glowing with {emotion}. "
    "Without thinking, they {verb} exactly {number} times... and the world was never the same again. 🌍",

    "{name} embarked on a journey to {place} 🌄 to find the legendary {magical_object} 🗝️. "
    "Fueled by {emotion}, they {verb} {number} times to overcome obstacles. 🏃‍♂️",

    "In the bustling city of {place} 🏙️, {name} accidentally unleashed the power of the {magical_object} 💥. "
    "Feeling {emotion}, they {verb} {number} times, causing chaos. 🚨"
]

# Randomly select a template
template = random.choice(templates)

# Fill the template with user inputs
story = template.format(name=name, place=place, magical_object=magical_object, emotion=emotion, verb=verb, number=number)

# Display the story
print("\nYour Story:\n")
print(story)

# Ask to save the story
save = input("\nDo you want to save this story to a file? (yes/no) ").strip().lower()
if save == 'yes':
    with open("story.txt", "w", encoding="utf-8") as file:
        file.write(story)
    print("Story saved to story.txt")
else:
    print("Okay, story not saved.")