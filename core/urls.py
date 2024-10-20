from django.urls import path

from .views import CategoryListCreateApiView, ProductListCreateView, \
    ProductGetUpdateView, VariantListCreateView, VariantDetailsView, \
    AttributeCreateView, AttributeDetailsView, AddCartView, CartView, \
    RemoveCartView, UpdateCartView, PaymentView


urlpatterns = [
    path('categories', CategoryListCreateApiView.as_view(), name='list_create_category'),

    path('products', ProductListCreateView.as_view(),
         name='list_create_product'),
    path('products/<str:id>', ProductGetUpdateView.as_view(),
         name='get_update_delete_products'),
    path('products/<str:product_id>/variant', VariantListCreateView.as_view(), name='create_list_variant'),
    path('products/<str:product_id>/variant/<str:id>', VariantDetailsView.as_view(), name='get_update_delete_variant'),
    path('products/<str:product_id>/attribute', AttributeCreateView.as_view(), name='create_attribute'),
    path('products/<str:product_id>/attribute/<str:id>', AttributeDetailsView.as_view(), name='get_update_delete_attribute'),

    path('cart/add', AddCartView.as_view(), name='add_variant_in_cart'),
    path('cart/update', UpdateCartView.as_view(), name='update_item_in_cart'),
    path('cart/remove', RemoveCartView.as_view(), name='remove_item_in_cart'),
    path('cart', CartView.as_view(), name='list_cart'),

    path('payment', PaymentView.as_view(), name='payment'),
]


