import os
import pandas as pd
from dotenv import load_dotenv
from mistralai.sdk import Mistral




import json


load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
print(f"[DEBUG] Loaded MISTRAL_API_KEY: {api_key}")
client = Mistral(api_key=api_key)

def analyze_feedback_mistral(text):
    prompt = f"""
    Analyze the following employee feedback. Return JSON with:
    - sentiment: Positive, Neutral, or Negative
    - emotions: list of emotional tones (frustration, gratitude, burnout, stress)
    - topics: list of relevant topics (workload, manager, tools, pay)

    Feedback: "{text}"
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.complete(model="mistral-medium", messages=messages)
    try:
        return json.loads(response.choices[0].message.content.strip())
    except:
        return {"error": "Could not parse Mistral response"}


def generate_solution_mistral(feedback_text, analysis):
    """
    Generate an actionable solution using Mistral AI, given feedback text and its analysis.
    """
    analysis_str = json.dumps(analysis, indent=2)
    prompt = f"""
    An employee has submitted the following feedback:
    "{feedback_text}"
    
    Here is an analysis of the feedback (sentiment, emotion, topics, language, etc.):
    {analysis_str}
    
    Based on both the feedback and the analysis, suggest 2-3 specific, actionable interventions or recommendations (in bullet points) for HR or the manager to address the main issues. Be concise and actionable.
    """
    messages = [{"role": "user", "content": prompt}]
    try:
        response = client.chat.complete(model="mistral-medium", messages=messages)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI ERROR] Could not generate solution: {e}"

def process_feedback_csv(csv_path, analyzer=analyze_feedback_mistral):
    df = pd.read_csv(csv_path)
    results = []
    for _, row in df.iterrows():
        feedback = row.get("feedback", "")
        department = row.get("department", "Unknown")
        analysis = analyzer(feedback)
        analysis["department"] = department
        results.append(analysis)
    return results

def generate_summary_mistral(team_name, feedback_list):
    joined_feedback = "\n".join([f"- {fb}" for fb in feedback_list])
    prompt = f"""
    Summarize the following feedback from the {team_name} team. Include:
    - Overall mood
    - Recurring concerns
    - 1 HR action suggestion

    Feedback:
    {joined_feedback}
    """
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.complete(model="mistral-medium", messages=messages)
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # Demo: Analyze mock_feedback.csv and print actionable solutions
    mock_csv = "mock_feedback.csv"
    print("\n--- Mistral CSV Feedback Analysis ---\n")
    results = process_feedback_csv(mock_csv)
    for result in results:
        print(result)
    print("\n--- Actionable Solutions (Mistral) ---\n")
    feedbacks = [r.get("feedback", "") for r in pd.read_csv(mock_csv).to_dict(orient="records")]
    print(generate_solutions_mistral(feedbacks))
    print("\n--- Mistral Summary ---\n")
    print(generate_summary_mistral("All Teams", feedbacks))

    # Legacy test cases for backward compatibility
    test_cases = [
        "Feeling overwhelmed tbh, deadlines too close",
        "I love my team but manager barely listens",
        "Niko stressed bana, kazi ngumu sana",
        "Happy with my role, team is great!",
        "Hii kazi inanichokesha kabisa",
        "Yo, work’s dope but pay sucks",
        "Oh great, another useless meeting",
        "Mazingira ya kazi ni mbaya sana",
        ""
    ]

    print("\n--- Mistral Feedback Analysis ---\n")
    for feedback in test_cases:
        result = analyze_feedback(feedback)
        print(f"Text: {feedback}\nMistral Result: {result}\n")

    
    print("\n--- Weekly Summary ---\n")
    feedbacks = [f for f in test_cases if f.strip()]
    summary = generate_summary("General Team", feedbacks)
    print(summary)

