from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Patient, Messages, Rooms
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
from djforge_redis_multitokens.tokens_auth import MultiToken
from django.db.models import Q
from uuid import uuid4
import mimetypes
from tempfile import NamedTemporaryFile
from datetime import datetime
from hack.utils import notify

class Message(APIView):

    def post(self, request):
        sender = request.user
        roomId = request._json_body['roomId']
        room = Rooms.objects.get(id=roomId)
        if room.status == 'INACTIVE':
            Response("Visit has ended", 400)
        data = request._json_body
        message = Messages.objects.create(
            messageType='text',
            messageBody=data['message'],
            creator=sender,
            room=room,
            visit=room.visit 
        )
        mems = room.participants
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
                "scr": message.url,
                "formId": '',
                "status": '',
            }
        }
        for mem in mems:
            if sender.id!=mem:
                notify(data, channel=mem)
        data['msg']['self']=True
        return Response(data['msg'])

    def get(self, request):
        roomId = request.GET['roomId']
        user = request.user
        room = Rooms.objects.get(id=roomId)
        messages = Messages.objects.filter(room=room).order_by('sentAt')
        result = []
        heading = []
        for message in messages:
            bol = False
            if user.id == message.creator.id:
                bol = True
            result.append(
                {
                    "id": message.id,
                    "type": message.messageType,
                    "time": message.sentAt.strftime('%I:%M %p'),
                    "sender": message.creator.first_name + ' ' + message.creator.last_name,
                    "self": bol,
                    "data": {
                        "msg": message.messageBody,
                        "scr": message.url,
                        "formId": '',
                        "status": '',
                    }
                })
        for mem in room.participants:
            if str(mem) != str(request.user.id):
                u = User.objects.get(id=mem)
                heading.append(u.first_name + ' ' + u.last_name)
        res = {
            'data': result,
            'heading': ' ,'.join(heading),
            'subHeading': 'subHeading',
            'status': room.status
        }
        return Response(res)


class Attachment(APIView):

    def post(self, request):
        roomId = request.POST['roomId']

        sender = request.user
        room = Rooms.objects.get(id=roomId)
        mems = room.participants
        file_obj = request.FILES['file']
        content = file_obj.read()
        filepath = file_obj.name
        kind = mimetypes.guess_type(filepath)
        f = NamedTemporaryFile(delete=False)
        f.write(content)
        filename = f.name
        msg_type = kind[0]
        if kind[0] == 'application/pdf':
            msg_type = 'pdf'
        if kind[0].split('/')[0] == 'image' or kind[0].split('/')[0] == 'Image':
            msg_type = 'image'

        message = Messages.objects.create(
            messageType=msg_type,
            creator=sender,
            attachmentDisplayName=file_obj.name,
            localName=filename,
            room=room,
            visit=visit
        )
        mems = room.participants
        return Response('wow')


class Inbox(APIView):

    def get(self, request):
        user = request.user
        all_rooms = Rooms.objects.all()
        rooms = []
        for room in all_rooms:
            if str(user.id) in room.participants:
                rooms.append(room)
        result = {}
        result['data'] = []

        for room in rooms:
            payload = {}
            payload['roomId'] = room.id
            payload['mems'] = []
            payload['name'] = ''
            for mem in room.participants:
                if str(mem) != str(user.id):
                    u = User.objects.get(pk=mem)
                    payload['mems'].append(u.first_name + ' ' + u.last_name)
                    payload['name'] += u.first_name + ' ' + u.last_name
            last_message = Messages.objects.filter(
                room=room).order_by('-sentAt').first()
            payload['lmt'] = last_message.sentAt.strftime(
                '%I:%M %p')  # %Y-%m-%d %H:%M
            if last_message.messageType != 'text':
                payload['lm'] = 'Attachment'
            else:
                payload['lm'] = last_message.messageBody
            result['data'].append(payload)
        return Response(result)
