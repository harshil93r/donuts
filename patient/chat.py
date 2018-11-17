from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Patient, Message, Room
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
from djforge_redis_multitokens.tokens_auth import MultiToken
from django.db.models import Q
from uuid import uuid4
import mimetypes

class Message(APIView):
    def post(self, request, roomId):
        sender = request.user
        room = Room.objects.get(id=roomId)
        _id = uuid4().__str__()
        data = request._json_body
        message = Message.objects.create(
            _id=_id,
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
        room = Room.objects.get(id=roomId)
        mems = room.participants
        _id = uuid4().__str__()
        file_obj = request.FILES['file']
        content = file_obj.read()
        filepath = file_obj.name
        kind = mimetypes.guess_type(filepath)
        epoc = int(time.time())
        f = NamedTemporaryFile(delete=False)
        f.write(content)
        filename = f.name
        
        Message.objects.create(
            _id=_id,
            messageType=kind[0],
            creator=sender,
            attachmentDisplayName=file_obj.name,
            localName=filename
        )
        mems = room.participants
        return Response('wow')
        
class Inbox(APIView):
    def get(self, request):
        user = request.user
        all_rooms = Room.objects.all()
        rooms = []
        for room in all_rooms:
            if user.id in room.participants:
                rooms.append(room)
        result = {}
        result['data'] = []
        participants = []
        for room in rooms:
            for mem in room.participants:
                if mem!=user.id:
                    name = User.objects.get(pk=mem).first_name
                    participants.append(name)
        for room in rooms:
            payload = {}
            payload['roomId'] = room.id
            payload['mems'] = participants
            last_message = Message.objects.filter(room=room.id).order_by('-sentAt').first()
            payload['lmt'] = last_message.sentAt
            if last_message.messageType!='TXT':
                payload['lm'] = 'Attachment'
            else:
                payload['lm'] = last_message.messageBody
            result['data'].append(payload)
        return Response(result)
