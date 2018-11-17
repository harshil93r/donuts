from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Patient, Message, MessageUserGroup, MessageRecipient, MessageGroup
from rest_framework.response import Response
from django.db.utils import IntegrityError
from hack.utils import send_sms
from random import randrange
from djforge_redis_multitokens.tokens_auth import MultiToken
from django.db.models import Q


