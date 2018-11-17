from django.urls import path
from .views import SignUp, OTPVerify, Login, DoctorList
from .auth_views import SignUp, OTPVerify, Login, Me, DoctorList

urlpatterns = [
    path('signup', SignUp.as_view()),
    path('otp_verify', OTPVerify.as_view()),
    path('login', Login.as_view()),
    path('doctor_list', DoctorList.as_view()),
    path('me', Me.as_view()),
]
