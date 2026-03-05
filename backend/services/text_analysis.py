from textblob import TextBlob
import re

FILLERS = ["uh", "um", "like", "you know", "so", "actually", "basically", "literally", "well", "right", "okay", "yeah"]

def analyze_text(text, duration):
    """Comprehensive text analysis for speech feedback"""
    words = text.split()
    word_count = len(words)
    
    # Speaking pace
    wpm = (word_count / duration) * 60 if duration > 0 else 0
    
    # Count filler words
    filler_count = sum(text.lower().count(f) for f in FILLERS)
    filler_percentage = (filler_count / word_count) * 100 if word_count > 0 else 0
    
    # Sentiment analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    # Grammar analysis (simple error detection)
    grammar_errors = detect_grammar_errors(text)
    grammar_score = max(0, 100 - (len(grammar_errors) * 10))
    
    # Vocabulary analysis
    unique_words = len(set(word.lower() for word in words))
    vocabulary_diversity = (unique_words / word_count) * 100 if word_count > 0 else 0
    
    return {
        "wpm": round(wpm, 2),
        "fillers": filler_count,
        "filler_percentage": round(filler_percentage, 1),
        "sentiment": round(sentiment, 3),
        "word_count": word_count,
        "grammar_score": grammar_score,
        "grammar_errors": grammar_errors,
        "vocabulary_diversity": round(vocabulary_diversity, 1),
        "unique_words": unique_words
    }

def detect_grammar_errors(text):
    """Simple grammar error detection"""
    errors = []
    
    # Common grammar patterns to check
    patterns = [
        (r'\bi is\b', 'Subject-verb disagreement'),
        (r'\bwas\s+\w+ing\b', 'Incorrect past continuous'),
        (r'\bthere\s+is\s+\w+s\b', 'There is/are disagreement'),
        (r'\bdont\b', 'Missing apostrophe in "don\'t"'),
        (r'\bcant\b', 'Missing apostrophe in "can\'t"'),
        (r'\bwont\b', 'Missing apostrophe in "won\'t"'),
        (r'\bits\s+\w+ing\b', 'Possible "it\'s" vs "its" error'),
        (r'\byour\s+(going|coming|being)\b', 'Possible "you\'re" vs "your" error'),
    ]
    
    for pattern, error_type in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            errors.append(f"{error_type}: '{match}'")
    
    return errors[:5]  # Limit to 5 errors