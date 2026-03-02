def extract_keywords(text):
    # Dummy implementation
    return text.split()[:5]

def analyze_text(text):
    # Dummy implementation
    return {
        'word_count': len(text.split()),
        'char_count': len(text),
    }

def detect_sentiment(text):
    # Dummy implementation
    return 'Neutral' if 'neutral' in text else 'Positive' if 'good' in text else 'Negative'
