from django.urls import path

from .views import ListAllProducts, ListProductOfSeller, CreateProductAPI

urlpatterns = [
    path('', ListAllProducts.as_view()),
    path('me/', ListProductOfSeller.as_view()),
    path('create/', CreateProductAPI.as_view()),
]
