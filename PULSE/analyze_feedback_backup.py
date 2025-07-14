from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")
vader = SentimentIntensityAnalyzer()

def analyze_feedback(text):
    result = {}

    # 1. VADER Sentiment Score
    vader_scores = vader.polarity_scores(text)
    result["sentiment"] = round(vader_scores["compound"], 2)

    # 2. spaCy NLP pipeline
    doc = nlp(text)

    # 3. Extract topics (noun chunks or keywords)
    keywords = set()
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 2:
            keywords.add(chunk.text.lower())
    result["topics"] = list(keywords)

    # 4. Simple emotion inference (rule-based)
    if "burnout" in text.lower() or "tired" in text.lower():
        result["emotion"] = "burnout"
    elif "happy" in text.lower() or "grateful" in text.lower():
        result["emotion"] = "gratitude"
    elif "ignored" in text.lower() or "unheard" in text.lower():
        result["emotion"] = "frustration"
    else:
        result["emotion"] = "neutral"

    return result
