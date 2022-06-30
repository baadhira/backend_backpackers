from django.shortcuts import render
# from django.http.response import JsonResponse
# from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status,generics
from event.models import *
from event.serializers import *
from app.serializers import *
from app.models import *
from rest_framework.views import APIView
from rest_framework import filters,viewsets
# from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django.contrib.auth import get_user_model
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import action



class EventViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]

    permission_classes =[IsAuthenticated]
    serializer_class =EventSerializer
    queryset=Event.objects.all()
    filter_backends =[filters.SearchFilter,DjangoFilterBackend]
    filterset_fields =["author__id","description","event_name","location"]
    search_fields =["description","eventname","location"]

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =CommentSerializer
    queryset=Comment.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
    
class EventComments(generics.CreateAPIView):
    serializer_class=CommentSerializer
    permission_classes =[IsAuthenticated]
    def get(self,request,event_id=None):
        event=get_object_or_404(Event,pk=event_id)
        comments_data=self.serializer_class(
            event.comments,many=True,context={"request":request}
        ).data

        return Response(data=comments_data)
    def post(self,request,event_id=None):
        event=Event.objects.get(pk=event_id)
        serializer=CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(event=event,author=self.request.user)
            return Response(serializer.data,status=status.HTTP_201_NO_CONTENT)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,event_id):
        event=self.get_object(pk=event_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class JoinedEventsView(viewsets.ModelViewSet):
    serializer_class=JoinedeventsSerializer
    permission_classes =[IsAuthenticated]
    queryset=JoinedPeople.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
# GetJoinedeventsSerializer
class GetJoinedEventsView(viewsets.ModelViewSet):
    serializer_class=GetJoinedeventsSerializer
    permission_classes =[IsAuthenticated]
    queryset=JoinedPeople.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class ReportEventPost(viewsets.ModelViewSet):
    serializer_class=EventReportSerializerPost
    permission_classes =[IsAuthenticated]
    queryset=ReportEvent.objects.all()
    # def perform_create(self,serializer):
    #     serializer.save(user=self.request.user)
class ReportEvent(viewsets.ModelViewSet):
    serializer_class=EventReportSerializerGet
    permission_classes =[IsAuthenticated]
    queryset=ReportEvent.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)



# class JoinView(APIView):
#     def post(self,request,form=None,id=None):
#         new=request.data["data"]
#         print("new....",new)
#         event=Event.objects.get(pk=id)
#         print("event attenddess..",event.limit_attendees)
#         if event.limit_attendees>0:

#             user=self.request.user
#             if user.is_authenticated:

#                 if user in event.joiners.all():
#                     join=False
#                     event.joiners.remove(user)
#                     event.limit_attendees=event.limit_attendees+1
#                 else:
#                     join=True
#                     event.joiners.add(user) 
#                     event.limit_attendees=event.limit_attendees-1
        
#         return Response(new)





# # Create your views here.
# @api_view(['GET', 'POST', 'DELETE'])
# def event_list(request):
#     if request.method == 'GET':
#         event=EventModel.objects.all()
#         eventname=request.query_params.get('eventName',None)
#         if eventname is not None:
#             event=event.filter(eventName__icontains=eventname)
#         event_serializer=EventSerializer(event,many=True)
#         return Response(event_serializer.data)
#     elif request.method == 'POST':
        
#         event_serializer=EventSerializer(data=request.data)
#         if event_serializer.is_valid():
#             event_serializer.save()
#             return Response(event_serializer.data,status=status.HTTP_201_CREATED) 
#         return Response(event_serializer.data,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         count = EventModel.objects.all().delete()
#         return Response({'message':'{}Tutorials deleted successfully!!'.format(count[0])},status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET','PUT','DELETE'])
# def event_details(request,pk):
#     try:
#         event = EventModel.objects.get(pk=pk)
#     except EventModel.DoesNotExist:
#         return Response({'message':'The event does not exist'},status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         event_serializer =EventSerializer(event)
#         return Response(event_serializer.data)
    
#     elif request.method == 'PUT':
       
#         event_serializer =EventSerializer(event,data=request.data)
#         if event_serializer.is_valid():
#             event_serializer.save()
#             return Response(event_serializer.data)
#         return Response(event_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         event.delete()
#         return Response({'message':'Event deleted successfully!!'})

# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def attendEvent(request,pk):
#     current_user = request.user
#     other_user=User.objects.get(pk=pk) 
#     if other_user not in current_user.EventModel.attendees.all():
#         current_user.EventModel.attendees.add(other_user)
    
#     else:
#         current_user.EventModel.attendees.remove(other_user)
#     return Response({'attendees':'successfully'})

# class JoinersEventView(APIView):
#     def get(self,request,format=None,username=None):
#         to_user = Event.objects.get(username=username)
#         from_user=self.request.user
#         join=None
#         if from_user.is_authenticated:

#             if from_user != to_user:
#                 if from_user in to_user.joiners.all():
#                     follow=False
#                     from_user.joiners.remove
        



class EventCommentViewSet(ModelViewSet):
   
    permission_classes =[IsAuthenticated]
    queryset = EventComment.objects.all()
    
    serializer_class = EventCommentSerializer

    @action(detail=False)
    def roots(self, request):
        queryset = EventComment.objects.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class EventCommentPostViewSet(ModelViewSet):
   
    permission_classes =[IsAuthenticated]
    queryset = EventComment.objects.all()
    
    serializer_class = EventCommentPostSerializer

    @action(detail=False)
    def roots(self, request):
        queryset = EventComment.objects.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
