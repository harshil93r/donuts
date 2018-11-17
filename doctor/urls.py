from django.urls import path
from .views import SignUp, Me
from patient.auth_views import Login, OTPVerify
urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('me',Me.as_view())
]
