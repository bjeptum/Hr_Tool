

from django.urls import path, include
from PULSE.views import twilio_webhook, feedback_data_api, dashboard_view, send_test_message, api_login, employee_api, send_bot_message_api

urlpatterns = [
    path('api/feedback-data/', feedback_data_api, name='feedback-data-api'),
    path('api/employees/', employee_api, name='employee-api'),
    path('', dashboard_view, name='dashboard'),
    path('send-test/', send_test_message),
    path('twilio/webhook/', twilio_webhook, name='twilio_webhook'),
    path('twilio/webhook/', twilio_webhook),
    path('api/login/', api_login, name='api-login'),
    path('api/send-bot-message/', send_bot_message_api, name='send-bot-message-api'),
]
