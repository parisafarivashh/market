
from django.urls import path
from .consumer import UserConsumer


websocket_urlpatterns = [
    # route for MySyncConsumer
    path('ws/user/',UserConsumer.as_asgi()),
]
