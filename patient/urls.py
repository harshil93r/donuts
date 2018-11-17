from django.urls import path
from .auth_views import SignUp, OTPVerify, Login, Me, DoctorList, DoctorRequest, EndChat
from .chat import Message, Attachment, Inbox, Vid

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('doctor_list', DoctorList.as_view()),
    path('me', Me.as_view()),
    path('doctor_request', DoctorRequest.as_view()),
    path('chat/send_text', Message.as_view()),
    path('chat/send_file', Attachment.as_view()),
    path('inbox', Inbox.as_view()),
    path('chat/messages', Message.as_view()),
    path('endchat', EndChat.as_view()),
    path('vid', Vid.as_view())
]
