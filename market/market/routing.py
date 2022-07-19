from django.urls import path

from user.consumers import UserConsumer

websocket_urlpatterns = [
    path(r'ws/user', UserConsumer.as_asgi()),
]

