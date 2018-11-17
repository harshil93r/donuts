from django.urls import path
from .auth_views import SignUp, OTPVerify, Login, Me, DoctorList, DoctorRequest

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('doctor_list', DoctorList.as_view()),
    path('me', Me.as_view()),
    path('doctor_request', DoctorRequest.as_view())
]
