from django.urls import path

from .views import Login, SignUpView, WalletDetailAPIView, UserProfile, \
    LogoutAPIView

urlpatterns = [
    path('login/', Login.as_view()),
    path('signup/', SignUpView.as_view()),
    path('wallet/', WalletDetailAPIView.as_view(), name='wallet'),
    path('profile/', UserProfile.as_view()),
    path('logout/', LogoutAPIView.as_view()),
]
