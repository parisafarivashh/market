from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, SendOtpView, VerifyPhoneView, LoginView, \
    ListUserView

router = DefaultRouter()
router.register('phone', VerifyPhoneView, basename='verify_phone')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('otp', SendOtpView.as_view(), name='send_otp'),
    path('login', LoginView.as_view(), name='login'),
    path('all', ListUserView.as_view(), name='list_user'),
    path('', include(router.urls)),
]

