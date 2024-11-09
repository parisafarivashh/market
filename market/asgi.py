"""
ASGI config for market project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

from authorize.router import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        websocket_urlpatterns,
    )
})

