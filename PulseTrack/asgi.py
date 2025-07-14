"""
ASGI config for PulseTrack project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from PULSE.consumers import FeedbackConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PulseTrack.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/feedback/", FeedbackConsumer.as_asgi()),
        ])
    ),
})
