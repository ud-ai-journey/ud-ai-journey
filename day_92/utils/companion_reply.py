def doodle_reply(emotion):
    replies = {
        "Joy": "I love hearing about your happy days! Keep shining, little buddy!",
        "Sadness": "It's okay to feel sad sometimes. I'm here for you, always!",
        "Anger": "Even dragons get angry! Taking deep breaths helps. You're awesome!",
        "Fear": "You are so brave for sharing your feelings!",
        "Surprise": "Surprises make life magical! Thanks for telling me!",
        "Neutral": "Every day is special with you!"
    }
    return replies.get(emotion, "Thank you for sharing your day with me!") 