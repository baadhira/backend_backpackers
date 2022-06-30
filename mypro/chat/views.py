from django.shortcuts import render
from rest_framework.views import APIView
from .models import ConversationModel
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db.models import Q
from .serializers import *
from rest_framework.response import Response
# from response import HTTP_200, HTTP_201, HTTP_400
from rest_framework import status
# Create your views here.
# return Response(event_serializer.data,status=status.HTTP_201_CREATED) 
class Contacts(APIView):
    permission_classes =(AllowAny,)
    def get(self, request):
        user_id=request.GET["user_id"]
        data=ConversationModel.objects.filter(
            Q(user1__id=user_id) | Q(user2__id=user_id))
        return Response(ConversationSerializer(data,many=True).data,status=status.HTTP_200)
    
    def post(self,request):
        users=User.objects.filter(
            id__in=[
                request.data["params"]["user1"],
                request.data["params"]["user2"]
                ]
        )

        result=ConversationModel.objects.filter(
            Q(user1=users[0],user2=users[1]) | Q(user1=users[1],user2=users[0])
        )
        user=result[0]

        if not result:
            user=ConversationModel.objects.create(
                user1=users[0],user2=users[1]
            )
        return Response(ConversationSerializer(user).data,status=status.HTTP_201)

class UserContacts(APIView):
    permission_classes=(AllowAny,)

    def get(self, request):
        data=ConversationModel.objects.filter(
            Q(user1__id=request.GET["id"],) | Q(user2__id=request.GET["id"],)
        )
        return Response(ConversationSerializer(data,many=True).data,status=status.HTTP_200)