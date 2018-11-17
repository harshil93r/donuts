from django.urls import path
from .auth_views import SignUp, OTPVerify, Login, Me, DoctorList, DoctorRequest
from .chat import Message, Attachment, Inbox

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('doctor_list', DoctorList.as_view()),
    path('me', Me.as_view()),
    path('doctor_request', DoctorRequest.as_view()),
    path('chat/<str:roomId>/send_text',Message.as_view()),
    path('chat/<str:roomId>/send_file',Attachment.as_view()),
    path('inbox',Inbox.as_view()),
    path('chat/<str:roomId>/messages',Message.as_view())
]
