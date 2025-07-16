def generate_story(text, emotion):
    if emotion == "Joy":
        return f"Today was a golden day full of laughter and happiness. {text}"
    elif emotion == "Sadness":
        return f"Even on blue days, you showed courage. {text}"
    elif emotion == "Anger":
        return f"You felt fiery today, but every dragon learns to cool down. {text}"
    elif emotion == "Fear":
        return f"You faced your fears bravely. {text}"
    elif emotion == "Surprise":
        return f"Wow! What an amazing surprise! {text}"
    else:
        return f"Another wonderful day to remember. {text}" 