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


class Message(APIView):

    def post(self, request, roomId):
        sender = request.user
        room = Rooms.objects.get(id=roomId)
        if room.status =='INACTIVE':
            Response("Visit has ended",400)
        data = request._json_body
        message = Messages.objects.create(
            messageType='TXT',
            messageBody=data['message'],
            creator=sender,
            room=room
        )
        mems = room.participants
        return Response('wow')


class Attachment(APIView):

    def post(self, request, roomId):
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

        message = Messages.objects.create(
            messageType=kind[0],
            creator=sender,
            attachmentDisplayName=file_obj.name,
            localName=filename,
            room=room
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
            print()
            payload['lmt'] = last_message.sentAt.strftime('%Y-%m-%d %H:%M')
            if last_message.messageType != 'TXT':
                payload['lm'] = 'Attachment'
            else:
                payload['lm'] = last_message.messageBody
            result['data'].append(payload)
        return Response(result)
