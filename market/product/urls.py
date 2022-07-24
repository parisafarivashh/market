from django.urls import path

from .views import ListAllProducts, ListProductOfSeller, CreateProductAPI, \
    GetProduct, UpdateProduct

urlpatterns = [
    path('', ListAllProducts.as_view()),
    path('me', ListProductOfSeller.as_view()),
    path('create', CreateProductAPI.as_view()),
    path('<int:id>', GetProduct.as_view()),
    path('update/<int:id>', UpdateProduct.as_view()),
]
