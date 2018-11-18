from django.urls import path
from .views import SignUp, Me, Accept, Reject, AddDoctor, FormView
from patient.auth_views import Login, OTPVerify
from patient.chat import Inbox, Message
urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('me', Me.as_view()),
    path('accept', Accept.as_view()),
    path('reject', Reject.as_view()),
    path('inbox', Inbox.as_view()),
    path('add', AddDoctor.as_view()),
    path('form', FormView.as_view()),
    path('chat/send_text', Message.as_view()),
    path('chat/messages',Message.as_view())
]
