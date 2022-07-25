from django.urls import path, include

from .views import CreateItemOrder, UpdateMyItemOrder, OrderViewList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderViewList, basename='order')

urlpatterns = [
    path('item', CreateItemOrder.as_view()),
    path('item/<int:id>', UpdateMyItemOrder.as_view()),
    path('', include(router.urls)),

    # path('', ListOrderUser.as_view()),

]
