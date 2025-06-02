import random

def load_recipes():
    return {
        "easy": {
            "lemonade": {"lemon", "water", "sugar"},
            "sandwich": {"bread", "cheese", "ham"},
            "fruit salad": {"apple", "banana", "orange"}
        },
        "medium": {
            "pancake": {"flour", "milk", "egg", "sugar"},
            "chai": {"tea leaves", "milk", "water", "sugar"},
            "omelette": {"egg", "milk", "salt", "pepper"}
        },
        "hard": {
            "butter chicken": {"chicken", "butter", "tomato", "cream", "spices"},
            "sushi": {"rice", "fish", "seaweed", "soy sauce", "vinegar"},
            "tiramisu": {"mascarpone", "coffee", "ladyfingers", "cocoa", "sugar"}
        }
    }

def play_round(dish, correct_ingredients, score, total_rounds, round_num):
    print(f"\n🔍 Round {round_num}/{total_rounds}: Guess the ingredients for {dish.title()} (comma-separated):")
    try:
        user_input = input("Ingredients: ").lower().split(",")
        user_ingredients = {item.strip() for item in user_input if item.strip()}
        
        if user_ingredients == correct_ingredients:
            print("✅ Perfect! You’re a recipe detective! 🕵️‍♂️")
            return score + 1
        else:
            missing = correct_ingredients - user_ingredients
            extra = user_ingredients - correct_ingredients
            feedback = []
            if missing:
                feedback.append(f"Missing: {', '.join(sorted(missing))}")
            if extra:
                feedback.append(f"Extra: {', '.join(sorted(extra))}")
            print(f"❌ Close! The real ingredients are: {', '.join(sorted(correct_ingredients))}")
            if feedback:
                print("Feedback: " + "; ".join(feedback))
            return score
    except Exception as e:
        print(f"🚨 Error: Invalid input. Please use comma-separated ingredients.")
        return score

def main():
    print("🍳 Welcome to Reverse Engineer the Recipe! 🧁")
    recipes = load_recipes()
    
    # Choose difficulty
    difficulty = input("Choose difficulty (easy/medium/hard): ").lower().strip()
    if difficulty not in recipes:
        difficulty = "easy"
        print("Defaulting to easy mode.")
    
    # Initialize game
    score = 0
    rounds = 3
    available_dishes = list(recipes[difficulty].items())
    
    # Play rounds
    for round_num in range(1, rounds + 1):
        if not available_dishes:
            print("No more dishes available!")
            break
        dish, correct_ingredients = random.choice(available_dishes)
        available_dishes.remove((dish, correct_ingredients))  # Avoid repeating dishes
        score = play_round(dish, correct_ingredients, score, rounds, round_num)
    
    # Display final score
    print(f"\n🏆 Game Over! Your score: {score}/{rounds}")
    if score == rounds:
        print("Master Chef! 🍽️ You nailed every recipe!")
    elif score > 0:
        print("Great job, sous-chef! Keep practicing! 👨‍🍳")
    else:
        print("No worries, every chef starts somewhere! Try again! 🥄")

if __name__ == "__main__":
    try:
        main()
    except EOFError:
        print("🚨 Input interrupted. Exiting game.")