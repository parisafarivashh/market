from django.urls import path

from .views import CategoryListCreateApiView, ProductListCreateView, \
    ProductGetUpdateView, VariantListCreateView, VariantDetailsView


urlpatterns = [
    path('categories', CategoryListCreateApiView.as_view(),
         name='list_create_category'),
    path('products', ProductListCreateView.as_view(),
         name='list_create_product'),
    path('products/<str:id>', ProductGetUpdateView.as_view(),
         name='get_update_delete_products'),
    path('variant', VariantListCreateView.as_view(), name='create_list_variant'),
    path('variant/<str:id>', VariantDetailsView.as_view(), name='get_update_delete_variant')
]


