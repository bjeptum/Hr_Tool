import os
import sys
import time
import django

# Add the project root (where manage.py is) to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))
print('DEBUG: sys.path =', sys.path)
print('DEBUG: PROJECT_ROOT =', PROJECT_ROOT)
print('DEBUG: Files in PROJECT_ROOT:', os.listdir(PROJECT_ROOT))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PulseTrack.settings')
django.setup()

from PULSE.twilio_utils import send_whatsapp_message
from PULSE.models import Feedback
from PULSE.analyze_feedback import analyze_feedback

# --- CONFIG ---
PHONE_NUMBER = '+254707427850'  # Your phone number
WAIT_SECONDS = 120  # How long to wait for your reply (in seconds)

if __name__ == '__main__':
    print(f"Sending WhatsApp message to {PHONE_NUMBER}...")
    send_whatsapp_message(PHONE_NUMBER, {"1": "Hi! Please reply to this message with your feedback for PulseTrack testing."})
    print("Message sent. Please reply to the WhatsApp message now.")
    print(f"Waiting up to {WAIT_SECONDS} seconds for your reply...")

    feedback = None
    for _ in range(WAIT_SECONDS):
        feedback = Feedback.objects.filter(message__isnull=False, sentiment_score__isnull=False, detected_topics__isnull=False, ).order_by('-timestamp').first()
        if feedback and feedback.message and feedback.message.strip() != '' and feedback.message.lower() != 'hi! please reply to this message with your feedback for pulsetrack testing.':
            break
        time.sleep(1)

    if not feedback:
        print("No feedback received in time. Please try again.")
    else:
        print("\n--- Feedback Received ---")
        print(f"Message: {feedback.message}")
        print(f"Timestamp: {feedback.timestamp}")
        print("\n--- Analysis Result ---")
        result = analyze_feedback(feedback.message)
        for k, v in result.items():
            print(f"{k}: {v}")
        print("\nDone!")
