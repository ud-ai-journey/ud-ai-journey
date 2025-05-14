import random

def guess_truth_or_lie(sentiment, sentiment_score, tempo, has_fillers):
    """Guess if the statement is truthful or suspicious."""
    suspicion_score = 0
    
    # Sentiment: Negative or low-confidence positive = more suspicious
    if sentiment == "negative" or (sentiment == "positive" and sentiment_score < 0.7):
        suspicion_score += 2
    elif sentiment == "neutral":
        suspicion_score += 1
    
    # Tempo: Fast tempo = more suspicious
    if tempo == "fast":
        suspicion_score += 2
    
    # Filler words: Presence = more suspicious
    if has_fillers:
        suspicion_score += 1
    
    # Random factor for fun
    suspicion_score += random.randint(0, 1)
    
    # Threshold: >3 is suspicious
    is_suspicious = suspicion_score > 3
    
    verdict = "Suspicious 🧢" if is_suspicious else "Truthful ✅"
    feedback = (
        f"You *might* be hiding something... 🍪👀" if is_suspicious 
        else "Sounds legit! 😎"
    )
    
    return verdict, feedback