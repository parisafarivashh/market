from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CreateDirect, SendMessage, ListAllChat, ListMessageOfDirect, \
    DeleteOrUpdateMessage, SeenMessage

router = DefaultRouter()
router.register('list', ListAllChat, basename='chat-list')

urlpatterns = [
    path('', CreateDirect.as_view()),
    path('message', SendMessage.as_view()),
    path('message/<int:id>', DeleteOrUpdateMessage.as_view()),
    path('message/seen/<int:id>', SeenMessage.as_view()),
    path('<int:id>/message/', ListMessageOfDirect.as_view()),
    path('', include(router.urls)),
]
