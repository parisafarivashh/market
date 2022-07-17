from django.urls import path

from .views import AdminAPIView, AdminPermissionsAPIView, \
    SetPermissionForAdminAPIView, AdminProfileAPIView, APIColor, APICategory, \
    APISubCategory
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', AdminAPIView.as_view(), name='admin'),
    path('color/', APIColor.as_view(), name='color'),
    path('color/<int:id>/', APIColor.as_view(), name='color'),
    path('category/', APICategory.as_view(), name='category'),
    path('category/<int:id>/', APICategory.as_view(), name='category'),
    path('sub-category/', APISubCategory.as_view(), name='sub-category'),
    path('sub-category/<int:id>/', APISubCategory.as_view(), name='single-sub-category'),
    path('profile/', AdminProfileAPIView.as_view(), name='admin-profile'),
    path('<int:id>/', AdminAPIView.as_view(), name='single-admin'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('permissions/', AdminPermissionsAPIView.as_view(), name='permissions'),
    path('permission/<int:id>/', SetPermissionForAdminAPIView.as_view(), name='permission_admin'),

]
