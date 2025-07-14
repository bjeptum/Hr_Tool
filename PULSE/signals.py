from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Feedback)
def handle_critical_feedback(sender, instance, created, **kwargs):
    if created and instance.sentiment_score < -0.7:
        # Send email alert
        subject = f"Critical Feedback Alert: {instance.department}"
        message = f"""
        Critical feedback detected in {instance.department} department.

        Message: {instance.raw_message}
        Sentiment Score: {instance.sentiment_score}
        Detected Topics: {', '.join(instance.detected_topics)}

        Time: {instance.timestamp}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [admin[0] for admin in settings.ADMINS],
            fail_silently=False,
        )