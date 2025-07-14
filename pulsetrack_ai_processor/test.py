import pandas as pd
from analyze_feedback import analyze_feedback
from mistral_ai_engine import generate_solutions_mistral, generate_summary_mistral

MOCK_CSV = "mock_feedback.csv"

df = pd.read_csv(MOCK_CSV)

print("\n--- Classic Feedback Analysis (mock_feedback.csv) ---\n")
classic_results = []
feedbacks = []
for i, row in df.iterrows():
    feedback = row.get("feedback", "")
    department = row.get("department", "Unknown")
    result = analyze_feedback(feedback)
    result["department"] = department
    print(f"Feedback: {feedback}\nAnalysis: {result}\n")
    classic_results.append(result)
    feedbacks.append(feedback)

print("\n--- Mistral Actionable Solutions ---\n")
print(generate_solutions_mistral(feedbacks))

print("\n--- Mistral Weekly Summary ---\n")
print(generate_summary_mistral("All Teams", feedbacks))
