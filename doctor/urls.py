from django.urls import path
from .views import SignUp, Me, Accept, Reject
from patient.auth_views import Login, OTPVerify
from patient.chat import Inbox
urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('me', Me.as_view()),
    path('accept', Accept.as_view()),
    path('reject', Reject.as_view()),
    path('inbox', Inbox.as_view())
]
