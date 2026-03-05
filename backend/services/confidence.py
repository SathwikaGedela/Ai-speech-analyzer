def calculate_confidence(metrics):
    wpm = metrics["wpm"]
    fillers = metrics["fillers"]
    sentiment = metrics["sentiment"]
    
    score = 100
    
    # WPM penalties/bonuses
    if wpm < 130:
        score -= (130 - wpm) * 0.5
    elif wpm > 160:
        score -= (wpm - 160) * 0.5
    
    # Filler word penalty
    score -= fillers * 2
    
    # Sentiment adjustment
    if sentiment < 0:
        score -= abs(sentiment) * 20
    elif sentiment > 0:
        score += sentiment * 10
    
    return max(0, min(100, round(score)))