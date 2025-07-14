from textblob import TextBlob
from transformers import pipeline

# Mock solution generator (replace with Mistral AI or LLM call in production)
from pulsetrack_ai_processor.mistral_ai_engine import generate_solution_mistral

def generate_solution(feedback_text, analysis):
    """
    Generate an actionable solution/recommendation for the given feedback using Mistral AI.
    Falls back to mock logic if Mistral is unavailable or returns an error.
    """
    solution = generate_solution_mistral(feedback_text, analysis)
    if solution and not solution.startswith('[AI ERROR]'):
        return solution
    # Fallback to legacy logic
    if analysis.get('sentiment_score', 0) < -0.5:
        return "We recommend scheduling a 1:1 with your manager or HR to discuss your concerns."
    if 'workload' in analysis.get('topics', []):
        return "Consider delegating tasks or requesting deadline extensions."
    if 'mental health' in analysis.get('topics', []):
        return "Take advantage of our mental health resources and consider a wellness break."
    if analysis.get('sentiment_label') == 'positive':
        return "Keep up the great work! Share your positivity with your team."
    return "Thank you for your feedback. We are reviewing it for further action."

def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def extract_topics(text):
    keywords = ["workload", "manager", "pay", "team", "tools"]
    found_topics = [word for word in keywords if word in text.lower()]
    return found_topicscr

def analyze_sentiment_advanced(text):
    classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
    return classifier(text)[0]['score'] * (1 if classifier(text)[0]['label'] == 'POSITIVE' else -1)
