from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from django.db.utils import IntegrityError
from patient.models import *
from rest_framework.response import Response
from hack.utils import send_sms
from random import randrange
import time
from hack.utils import notify as socket_notify
from django.conf import settings
# Create your views here.


class SignUp(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        body = request._json_body
        u = User(
            first_name=body['fn'],
            last_name=body['ln'],
            _type='DOC',
            phoneNo=body['phoneNo'],
            username=body['phoneNo']
        )
        try:
            u.save()
        except IntegrityError:
            u = User.objects.get(phoneNo=body['phoneNo'])
            if u.status == 2:
                return Response({'error': 'doctor already signedup'}, 400)
        u.set_password(body['password'])
        _otp = randrange(1000, 9999)
        u.otp = _otp
        u.save()
        sms_text = 'Your OTP is {otp} please use this to verify'.format(
            otp=_otp)
        send_sms(sms_text, body['phoneNo'])
        return Response({'status': 'otp sent'})


class Me(APIView):

    def get(self, request):
        u = request.user
        res = {'fn': u.first_name,
               'ln': u.last_name,
               'status': u.status, 'userId': u.id}
        return Response(res)

    def patch(self, request):
        body = request._json_body
        u = request.user
        d = Doctor(
            price=body['price'],
            speciality=body['speciality'],
            pcpId=body['pcpId'],
            license=body['license'],
            insuaranceNo=body['insuaranceNo']
        )
        d.save()
        u.status = 3
        u._type = 'DOC'
        u.doctor = d
        u.save()
        return Response({})


class Accept(APIView):

    def post(self, request):
        body = request._json_body
        u = request.user
        visit = Visit.objects.get(id=body['visit_id'])
        if visit.status != 'PENDING':
            return Response({'error': 'already accepted.'}, 400)
        # if visit.type == 'ALL':
        visit.doctor.append(u.id)
        visit.status = 'STARTED'
        visit.save()
        paticipant = []
        paticipant.append(u.id)
        paticipant.append(visit.patient.id)
        print(paticipant)
        try:
            room = Rooms.objects.get(participants=paticipant)
            room.status = 'ACTIVE'
        except Rooms.DoesNotExist:
            room = Rooms(
                participants=paticipant,
                status='ACTIVE',
                visit=visit
            )
            room.save()
        room.visit = visit
        room.save()
        message = Messages.objects.create(
            messageType='info',
            messageBody='visit has started at {}'.format(
                time.strftime('%dth %b, %I:%M %p')),
            creator=u,
            room=room,
            visit=visit
        )
        push_data = {
            'action': 1,
            'roomId': room.id,
            'eventType': 'doctor_request'
        }
        socket_notify(push_data, channel=visit.patient.id)
        socket_notify(push_data, channel=u.id)
        return Response({'roomId': room.id})


class Reject(APIView):

    def post(self, request):
        body = request._json_body
        u = request.user
        visit = Visit.objects.get(id=body['visit_id'])
        if visit.type == 'SPECIFIC':
            push_data = {
                'action': 2,
            }
            socket_notify(push_data, channel=visit.patient.id)
            return Response(response)
        else:
            pass


class AddDoctor(APIView):

    def post(self, request):
        body = request._json_body
        u = request.user
        room = Rooms.objects.get(id=body['roomId'])
        message = Messages.objects.create(
            messageType='info',
            messageBody='This chat has been shifted to different room',
            creator=u,
            room=room,
            visit=room.visit
        )
        room.participants.append(body['userId'])
        visit = Visit.objects.get(id=room.visit_id)
        try:
            User.objects.get(id=body['userId'])
        except:
            return Response({'error': 'invalid userId'}, 400)
        visit.doctor.append(body['userId'])
        visit.status = 'ENDED'
        visit.save()
        v = Visit(
            patient=visit.patient,
            status='STARTED',
            type='ALL',
            doctor=visit.doctor
        )
        v.save()
        try:
            roomnew = Rooms.objects.get(participants=room.participants)
            roomnew.visit = v
            roomnew.save()
        except Rooms.DoesNotExist:
            roomnew = Rooms(
                participants=room.participants,
                status='ACTIVE',
                visit=v
            )
            roomnew.save()
        push_data = {
            'action': 1,
            'roomId': roomnew.id,
            'eventType': 'doctor_request'
        }
        messes = Messages.objects.filter(visit_id=visit.id)
        for mess in messes:
            message = Messages.objects.create(
                messageType=mess.messageType,
                messageBody=mess.messageBody,
                creator=mess.creator,
                room=roomnew,
                visit=v
            )
        message = Messages.objects.create(
            messageType='info',
            messageBody='Doctor is added to chat',
            creator=u,
            room=roomnew,
            visit=v
        )

        for par in roomnew.participants:
            print(par)
            socket_notify(push_data, channel=par)
        return Response({'roomId': roomnew.id})


class FormView(APIView):

    def get(self, request):
        return Response(['formA', 'formB', 'formC'])

    def post(self, request):
        body = request._json_body
        u = request.user
        room = Rooms.objects.get(id=body['roomId'])
        form = Form.objects.create(
            formType=body['formType'],
            status='PENDING',
            createdBy=u
        )
        message = Messages.objects.create(
            messageType='form',
            messageBody='Please fill this form',
            creator=u,
            room=room,
            visit=room.visit,
            formId=form.id
        )
        data = {}
        data['eventType'] = 'new_chat_message'
        data['msg'] = {
            "id": message.id,
            "type": message.messageType,
            "time": message.sentAt.strftime('%I:%M %p'),
            "sender": message.creator.first_name + ' ' + message.creator.last_name,
            "self": False,
            "data": {
                "msg": message.messageBody,
                "scr": '',
                "formId": form.id,
                "status": form.status,
            }
        }
        for par in room.participants:
            if par != str(u.id):
                socket_notify(data, channel=par)
        data['msg']['self'] = True
        return Response(data)
