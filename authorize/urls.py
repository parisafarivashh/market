from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, SendOtpView, VerifyPhoneView, LoginView

router = DefaultRouter()
router.register('phone', VerifyPhoneView, basename='verify_phone')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('otp', SendOtpView.as_view(), name='send_otp'),
    path('login', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]

