from django.urls import path

from .views import RegisterView, SendOtpView


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('otp', SendOtpView.as_view(), name='send_otp'),
]

