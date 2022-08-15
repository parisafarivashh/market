from django.urls import path

from user.consumers import UserConsumer
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path(r'ws/user-notif', UserConsumer.as_asgi()),
    path(r'ws/direct/<int:id>', ChatConsumer.as_asgi()),
]

