from django.urls import path

from .views import CategoryListCreateApiView, ProductListCreateView, \
    ProductGetUpdateView, VariantListCreateView, VariantDetailsView, \
    AttributeCreateView


urlpatterns = [
    path('categories', CategoryListCreateApiView.as_view(),
         name='list_create_category'),
    path('products', ProductListCreateView.as_view(),
         name='list_create_product'),
    path('products/<str:id>', ProductGetUpdateView.as_view(),
         name='get_update_delete_products'),
    path('products/<str:product_id>/variant', VariantListCreateView.as_view(), name='create_list_variant'),
    path('products/<str:product_id>/variant/<str:id>', VariantDetailsView.as_view(), name='get_update_delete_variant'),
    path('products/<str:product_id>/attribute', AttributeCreateView.as_view(), name='create_attribute')
]


