from django.urls import path
from .auth_views import SignUp, OTPVerify, Login, Me

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('me', Me.as_view())
]
