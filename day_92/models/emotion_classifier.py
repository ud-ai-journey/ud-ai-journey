# Simple offline-friendly emotion classifier (placeholder)
def classify_emotion(text):
    text = text.lower()
    if any(word in text for word in ["happy", "fun", "joy", "excited", "love"]):
        return "Joy", "Yellow", "🌞"
    elif any(word in text for word in ["sad", "cry", "upset", "unhappy", "down"]):
        return "Sadness", "Blue", "💧"
    elif any(word in text for word in ["angry", "mad", "furious", "annoyed"]):
        return "Anger", "Red", "🔥"
    elif any(word in text for word in ["scared", "afraid", "fear", "nervous"]):
        return "Fear", "Purple", "😨"
    elif any(word in text for word in ["surprised", "amazed", "wow"]):
        return "Surprise", "Orange", "🎉"
    else:
        return "Neutral", "Green", "🟢" 