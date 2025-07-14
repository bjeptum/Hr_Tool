from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import spacy
import pandas as pd
from langdetect import detect
from collections import Counter

# Initialize models
vader = SentimentIntensityAnalyzer()
nlp = spacy.load("en_core_web_sm")

# Expanded emotion and topic mappings
custom_emotion_map = {
    # English (negative emotions prioritized)
    "manager": "frustration", "unheard": "frustration", "ignored": "frustration", "unappreciated": "frustration", 
    "sucks": "frustration", "useless": "frustration", "waste": "frustration", "pointless": "frustration",
    "burnout": "burnout", "tired": "burnout", "overwhelmed": "burnout", "exhausted": "burnout", "burnt": "burnout", "af": "burnout",
    "stressed": "stress", "stress": "stress", "pressure": "stress", "anxiety": "stress", "sana": "stress",
    # Kiswahili
    "nimechoka": "burnout", "kazi ngumu": "stress", "hanielewi": "frustration",
    "mbaya": "stress", "akili": "stress", "bana": "stress", "msongo": "stress",
    "shida": "stress", "msongo wa mawazo": "stress", "inanichokesha": "burnout",
    # English (positive emotions last)
    "happy": "gratitude", "grateful": "gratitude", "love": "gratitude", "awesome": "gratitude", "dope": "gratitude"
}

topic_map = {
    # English
    "deadline": "workload", "deadlines": "workload", "work": "workload", "task": "workload", "tasks": "workload",
    "manager": "manager", "boss": "manager", "supervisor": "manager", "management": "manager",
    "team": "team", "colleagues": "team", "coworkers": "team", "teammates": "team",
    "pay": "salary", "salary": "salary", "compensation": "salary", "wages": "salary",
    "stress": "mental health", "burnout": "mental health", "anxiety": "mental health", "burnt": "mental health", "af": "mental health",
    # Kiswahili
    "kazi": "workload", "hanielewi": "manager", "akili": "mental health",
    "mbaya": "mental health", "msongo": "mental health", "shida": "mental health", "inanichokesha": "workload"
}

def analyze_sentiment(text):
    """Analyze sentiment using VADER. Return score and label."""
    scores = vader.polarity_scores(text)
    compound = round(scores["compound"], 2)
    # Adjust score for negative keywords
    negative_words = ["useless", "another", "waste", "pointless", "barely", "sucks", "overwhelmed", "burnt", "af"]
    if any(word in text.lower() for word in negative_words):
        compound = round(min(compound - 0.3, -0.1), 2)  # Boost negativity, round to 2 decimals
    # Adjusted thresholds for better sensitivity
    if compound >= 0.1:
        label = "positive"
    elif compound <= -0.1:
        label = "negative"
    else:
        label = "neutral"
    return compound, label

def detect_emotion(text):
    """Detect emotion using keyword mapping, prioritizing negative emotions."""
    text_lower = text.lower()
    # Check negative emotions first
    negative_emotions = {k: v for k, v in custom_emotion_map.items() if v in ["frustration", "burnout", "stress"]}
    for keyword, emotion in negative_emotions.items():
        if keyword in text_lower:
            return emotion
    # Then check positive emotions
    positive_emotions = {k: v for k, v in custom_emotion_map.items() if v == "gratitude"}
    for keyword, emotion in positive_emotions.items():
        if keyword in text_lower:
            return emotion
    return "neutral"

def extract_topics(text):
    """Extract topics using spaCy noun chunks and mapping."""
    doc = nlp(text.lower())
    topics = set()
    # Check noun chunks
    for chunk in doc.noun_chunks:
        for keyword, topic in topic_map.items():
            if keyword in chunk.text:
                topics.add(topic)
    # Check individual tokens
    for token in doc:
        for keyword, topic in topic_map.items():
            if keyword == token.text:
                topics.add(topic)
    # Ensure mental health is added if stress or burnout emotions are detected
    if detect_emotion(text) in ["stress", "burnout"]:
        topics.add("mental health")
    return list(topics) if topics else ["other"]

def detect_language(text):
    """Detect text language using langdetect, with fallback for mixed inputs."""
    try:
        # Check for Kiswahili keywords to improve detection
        sw_keywords = ["kazi", "nimechoka", "hanielewi", "mbaya", "akili", "bana", "msongo", "shida", "inanichokesha", "sana"]
        if any(kw in text.lower() for kw in sw_keywords):
            return "sw"
        lang = detect(text)
        return "sw" if lang == "sw" else "en"
    except:
        return "unknown"

def analyze_feedback(text):
    """Analyze feedback text and return sentiment, emotion, topics, and language."""
    if not text or not text.strip():
        return {
            "sentiment_score": 0.0,
            "sentiment_label": "neutral",
            "emotion": "neutral",
            "topics": ["other"],
            "language": "unknown"
        }
    score, label = analyze_sentiment(text)
    return {
        "sentiment_score": score,
        "sentiment_label": label,
        "emotion": detect_emotion(text),
        "topics": extract_topics(text),
        "language": detect_language(text)
    }

def process_feedback_csv(csv_path):
    """Read CSV with feedback + department and return enriched feedback data."""
    df = pd.read_csv(csv_path)
    results = []
    for _, row in df.iterrows():
        feedback = row.get("feedback", "")
        department = row.get("department", "Unknown")
        analysis = analyze_feedback(feedback)
        analysis["department"] = department
        results.append(analysis)
    return results

def generate_summary(results):
    """Generate a simple summary of top topics and average sentiment."""
    if not results:
        return "No feedback data available."
    topic_counts = Counter()
    sentiment_sum = 0
    for result in results:
        for topic in result["topics"]:
            topic_counts[topic] += 1
        sentiment_sum += result["sentiment_score"]
    avg_sentiment = round(sentiment_sum / len(results), 2)
    top_topic = topic_counts.most_common(1)[0][0] if topic_counts else "none"
    return f"Top issue: {top_topic}. Average sentiment: {avg_sentiment}"

if __name__ == "__main__":
    # Sample test cases
    test_cases = [
        "Feeling overwhelmed tbh, deadlines too close",
        "I love my team but manager barely listens",
        "Niko stressed bana, kazi ngumu sana",
        "Happy with my role, team is great!",
        "Hii kazi inanichokesha kabisa",
        "Yo, work’s dope but pay sucks",
        "Oh great, another useless meeting",
        "Mazingira ya kazi ni mbaya sana",
        ""  # Added empty input test
    ]

    print("\n--- Single Feedback Analysis ---\n")
    for text in test_cases:
        result = analyze_feedback(text)
        print(f"Text: {text}\nResult: {result}\n")

    # CSV processing demo
    print("\n--- CSV Feedback Analysis ---\n")
    try:
        results = process_feedback_csv("mock_feedback.csv")
        for result in results:
            print(result)
        print("\n--- Summary ---\n")
        print(generate_summary(results))
    except FileNotFoundError:
        print("mock_feedback.csv not found. Please create it with 'feedback' and 'department' columns.")