"""
ASGI config for market project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from authorize.router import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
django.setup()

from market.authentication_ws import JWTAuthMiddlewareStack


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})

