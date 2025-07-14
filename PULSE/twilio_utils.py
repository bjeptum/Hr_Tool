from celery import shared_task
from PULSE.models import Employee, FeedbackConfig
from datetime import datetime
from .twilio_integration import send_whatsapp_message


@shared_task
def send_scheduled_checkins():
    today = datetime.now().date()

    # For weekly: Monday, biweekly: alternate weeks
    if today.weekday() == 0:  # Monday
        for config in FeedbackConfig.objects.all():
            frequency = config.frequency
            if frequency == 'biweekly' or \
                    (frequency == 'weekly') or \
                    (frequency == 'biweekly' and today.isocalendar()[1] % 2 == 0):

                for employee in Employee.objects.filter(
                        department=config.department,
                        is_active=True
                ):
                    send_whatsapp_message(
                        employee.phone,
                        {"1": "\n".join(config.questions)}
                    )