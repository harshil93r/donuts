from django.urls import path
from .views import SignUp, OTPVerify

urlpatterns = [
    path('/signup', SignUp.as_view()),
    path('/otp_verify', OTPVerify.as_view()),
]
