from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    phone_number = models.CharField(max_length=20, unique=True, default="0000000000")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.phone

class FeedbackConfig(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'),
    ], default='weekly')
    questions = models.JSONField(default=list)

    def __str__(self):
        return f"{self.department} - {self.frequency}"

class Feedback(models.Model):
    raw_message = models.TextField(default="No message")
    sentiment_score = models.FloatField()
    detected_topics = models.JSONField(default=list)
    source_number = models.CharField(max_length=20, blank=True)
    media_url = models.URLField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    solution = models.TextField(blank=True, null=True, default="")  # Stores AI-generated solution

    def __str__(self):
        return f"Feedback ({self.timestamp:%Y-%m-%d %H:%M})"