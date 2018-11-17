from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response


# Create your views here.
class SignUp(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        pass
