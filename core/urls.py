from django.urls import path

from .views.category import CategoryListCreateApiView


urlpatterns = [
    path('categories', CategoryListCreateApiView.as_view(),
         name='list_create_category'),
]

