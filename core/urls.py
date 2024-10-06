from django.urls import path

from .views import CategoryListCreateApiView, ProductListCreateView

urlpatterns = [
    path('categories', CategoryListCreateApiView.as_view(),
         name='list_create_category'),
    path('products', ProductListCreateView.as_view(),
         name='list_create_product'),
]


