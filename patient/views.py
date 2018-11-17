
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
# Create your views here.


class SignUp(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = request._json_body
        u = User(
            first_name=body['fn'],
            last_name=body['ln'],
            phoneNo=body['phoneNo']
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

        return Response('hello')


class DoctorList(APIView):

    def get(self, request):
        user = request.user
        doctors = User.objects.filter(patient=None).exclude(doctor__pcpId=user.patient.pcpId)
        pcp = User.objects.filter(doctor__pcpId=user.patient.pcpId)

        r = {}
        r['pcp'] = {}
        r['cir'] = {}
        r['oth'] = {}
        payload = {}
        payload['pcpId'] = pcp.doctor.pcpId
        payload['name'] = pcp.first_name + pcp.last_name
        payload['rating'] = pcp.doctor.rating
        payload['price'] = pcp.doctor.price
        payload['speciality'] = pcp.doctor.price
        r['pcp'].append(payload)
        for doc in doctors:
            if doc.zip5==user.zip5:
                payload['pcpId'] = doc.doctor.pcpId
                payload['name'] = doc.first_name + doc.last_name
                payload['rating'] = doc.doctor.rating
                payload['price'] = doc.doctor.price
                payload['speciality'] = doc.doctor.speciality
                r['cir'].append(payload)
            else:
                payload['pcpId'] = doc.doctor.pcpId
                payload['name'] = doc.first_name + doc.last_name
                payload['rating'] = doc.doctor.rating
                payload['price'] = doc.doctor.price
                payload['speciality'] = doc.doctor.speciality
                r['oth'].append(payload)

        return Response(r)