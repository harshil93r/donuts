
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
from djforge_redis_multitokens.tokens_auth import MultiToken
import json
import ast
# Create your views here.


class SignUp(APIView):
    permission_classes = ()
    authentication_classes = ()
    def post(self, request):
        body = request._json_body
        u = User(
            first_name=body['fn'],
            last_name=body['ln'],
            phoneNo=body['phoneNo'],
            username=body['phoneNo']
        )
        try:
            u.save()
        except IntegrityError:
            u = User.objects.get(phoneNo=body['phoneNo'])
            if u.status == 2:
                return Response({'error': 'patient already signedup'})
        u.set_password(body['password'])
        _otp = randrange(1000, 9999)
        u.otp = _otp
        u.save()
        sms_text = 'Your OTP is {otp} please use this to verify'.format(
            otp=_otp)
        send_sms(sms_text, body['phoneNo'])
        return Response({'status': 'otp sent'})


class OTPVerify(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = request._json_body
        return Response('hello')

class Login(APIView):
    permission_classes = ()
    authentication_classes = ()
    def post(self, request):
        try:
            _username = request._json_body['username']
            _password = request._json_body['password']
        except KeyError as e:
            raise BadRequest(str(e) + ' is required in request body.')
        _user = User.objects.get(phoneNo=_username)
        if not _user:
            raise BadRequest('username or password seems incorrect.')
        if not _user.check_password(_password):
            locked_response = Response(
                {
                    "error": {"message": "Account Locked.", "code": -1},
                    "statusCode": 400,
                }, 400,
            )
            return locked_response
        token, _ = MultiToken.create_token(_user)
        response_data = {
            'loggedInAlready': _,
            'token': token.key,
        }
        user_data_map = {
            'firstName': 'first_name',
            'lastName': 'last_name',
            'userId': 'app_user_id',
            'empi': 'app_user_id',
            # 'updatedOn': 'updated_on',
            'gender': 'gender',
        }
        return Response(response_data)
