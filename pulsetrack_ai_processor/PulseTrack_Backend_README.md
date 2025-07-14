
# 📄 README: AI Feedback Analyzer Integration

### 🧠 Module: `analyze_feedback.py`  
**Author:** [Alvin Kariuki]  
**Role:** AI/NLP Engineer – PulseTrack Hackathon Project  
**Purpose:** Analyze raw employee feedback and return structured HR insights.

---

## 🚀 Overview

This NLP module processes natural-language feedback from employees (via SMS, WhatsApp, or chatbot) and returns:

- Sentiment Score (numeric)
- Sentiment Label (positive / neutral / negative)
- Emotion (e.g. burnout, stress, frustration, gratitude)
- Topics (e.g. workload, salary, manager)
- Language (en, sw, unknown)

---

## 📦 File Location

The module is in:  
```
/ai_pulsetrack/analyze_feedback.py
```

---

## 🔌 How to Use the Module

### ✅ 1. Import the Function

```python
from analyze_feedback import analyze_feedback
```

### ✅ 2. Call the Function

```python
feedback_text = "I'm overwhelmed. Boss hanielewi bana."
result = analyze_feedback(feedback_text)
```

### ✅ 3. Sample Output

```json
{
  "sentiment_score": -0.4,
  "sentiment_label": "negative",
  "emotion": "burnout",
  "topics": ["manager", "workload", "mental health"],
  "language": "sw"
}
```

---

## 🔁 Full Integration Flow

### 🔽 From Bot to Storage:

1. Employee sends feedback via WhatsApp/SMS  
2. Bot receives the message, sends it to Django via webhook  
3. Django backend receives raw message, stores it temporarily or directly  
4. Immediately call `analyze_feedback()` to process the message  
5. Save both the raw and analyzed data to the database  
6. Frontend reads from DB to show sentiment heatmaps, charts, etc.

---

## 💾 Suggested Django Model

```python
class Feedback(models.Model):
    text = models.TextField()
    department = models.CharField(max_length=100)
    sentiment_score = models.FloatField()
    sentiment_label = models.CharField(max_length=20)
    emotion = models.CharField(max_length=50)
    topics = models.JSONField()  # List of strings
    language = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)
```

---

## 🔧 Example Django View

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from analyze_feedback import analyze_feedback
import json

@csrf_exempt
def receive_feedback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get("feedback", "")
        department = data.get("department", "General")

        analysis = analyze_feedback(text)

        # Save to DB (assuming Feedback model is defined)
        Feedback.objects.create(
            text=text,
            department=department,
            sentiment_score=analysis["sentiment_score"],
            sentiment_label=analysis["sentiment_label"],
            emotion=analysis["emotion"],
            topics=analysis["topics"],
            language=analysis["language"]
        )

        return JsonResponse(analysis)

    return JsonResponse({"error": "POST method required"}, status=405)
```

---

## 🧪 Test the Module

You can run the module directly with built-in test cases:

```bash
python analyze_feedback.py
```

Or test it with your own CSV:

```bash
# Create a file named mock_feedback.csv:
feedback,department
"I'm tired of this job",Sales
"Boss hanielewi kabisa",Operations

# Then run:
python analyze_feedback.py
```

---

## 📌 Output Fields Explained

| Field              | Type   | Description                                  |
|-------------------|--------|----------------------------------------------|
| sentiment_score    | float  | VADER score (-1 to +1)                       |
| sentiment_label    | string | Human-readable tone: positive / neutral / negative |
| emotion            | string | Detected emotional state (burnout, stress, etc.) |
| topics             | list   | HR-related keywords extracted from the text  |
| language           | string | Detected language: "en", "sw", or "unknown"  |

---

## 💡 Notes & Assumptions

- Sentiment is based on VADER with sarcasm and frustration keyword handling.
- Emotion detection is rule-based using local language and slang.
- Topics are extracted using spaCy + keyword mapping.
- The module is offline and doesn't require API calls.
- Returns neutral defaults for blank feedback.
- Language detection supports English, Kiswahili, and mixed inputs.

---

## ❓ Support

For questions or help integrating, ping the AI/NLP lead.  
Future ideas:
- Add timestamped trends
- HR alerts for low morale
- Translation layer for non-English inputs

---

## 🎉 Let’s Win This Hackathon!

This module is fast, culturally aware, and battle-tested.  
Please ensure the frontend reads the fields: `sentiment_score`, `emotion`, `topics`, `department`.

