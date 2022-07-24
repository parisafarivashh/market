from django.urls import path

from .views import CreateItemOrder, UpdateMyOrder, ListOrderUser

urlpatterns = [
    path('item', CreateItemOrder.as_view()),
    path('item/<int:id>', UpdateMyOrder.as_view()),
    path('', ListOrderUser.as_view()),

]
