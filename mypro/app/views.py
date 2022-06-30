from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from app.serializers import *
from django.contrib.auth import authenticate
from app.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import *
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter
from rest_framework import filters,viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import FormParser, MultiPartParser


#to generate tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            print("user",user)
            return Response({'token':token,'msg':'Registration successful'})
            status = status.HTTP_201_CREATED
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
   renderer_classes = [UserRenderer]
   def post(self, request,format=None): 
       serializer = UserLoginSerializer(data=request.data)
    #    username1=request.data["username"]
    #    password1=request.data['password']
    #    print(username1,password1,"data from fronend ")
       if serializer.is_valid(raise_exception=True):
           username = serializer.data.get('username')
           password=serializer.data.get('password')
        #    print("username: " ,username)
        #    print("password: " ,password)
           user=authenticate(username=username,password=password)
        #    print(type(user))
        #    print("user: " ,user)
        #    print("pass" ,password)
        #    print("authnt")
           if user is not None :
               token = get_tokens_for_user(user)
               if user.is_admin:                
                    return Response({'token':token,'msg':'Admin Login successful',"is_admin":"is_admin"},status=status.HTTP_200_OK)    
            #    print("user in not none.....")
               return Response({'token':token,'msg':'Login successful',"is_admin":"not admin"},status=status.HTTP_200_OK)
           else:
            #    print("user is none////////")
               return Response({'errors':{'non_field errors':['username or password is not valid']}},status=status.HTTP_400_BAD_REQUEST)
       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes= [UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

        
class userAccount(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk) 
        except User.DoesNotExist:
            raise Http404 
    def get(self,request,pk,format=None):
        profile=self.get_object(pk)
        serializer=Accountserializer(profile)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        profile=self.get_object(pk)
        serializer=Accountserializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class PatchUser(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =Accountserializer
    queryset=User.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class userProfile(APIView):
    permission_classes=[IsAuthenticated]

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404 
    def get(self,request,pk,format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        profile=self.get_object(pk)
        serializer = ProfileSerializer(profile,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PatchProfile(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =ProfileSerializer
    queryset=User.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):
        serializer=UserchangePasswordSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordRestEmail(APIView):
    renderer_classes=[UserRenderer]

    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Send,Please Send Your Email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request,uid,token,format=None):
        serializer =UserPasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class AllUsers(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =UserList
    queryset=User.objects.all()
    filter_backends =[filters.SearchFilter,DjangoFilterBackend]
    filterset_fields =["first_name","last_name",'hosting_check','born_location']
    search_fields =["first_name","last_name",'hosting_check','born_location']

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

# class userAlbum(APIView):
#     def get_object(self,pk):
#         try:
#             return Album.objects.get(pk=pk)
#         except Album.DoesNotExist:
#             raise Http404 
#     def get(self,request,pk,format=None):
#         album = self.get_object(pk)
#         serializer = AlbumSerializer(album)
#         return Response(serializer.data)
    

#     def put(self,request,pk,format=None):
#         album=self.get_object(pk)
#         serializer = AlbumSerializer(album,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,pk,format=None):
#         album=self.get_object(pk)
#         album.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# class UserAlbumCreate(APIView):
#     def post(self,request,format=None):
#         serializer = AlbumSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AlbumViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes =[IsAuthenticated]
    serializer_class =AlbumSerializer
    queryset=Album.objects.all()
    # filter_backends =[filters.SearchFilter,DjangoFilterBackend]
    # filterset_fields =["author__id","description","event_name","location"]
    # search_fields =["description","eventname","location"]

    # def perform_create(self,serializer):
    #     serializer.save(author=self.request.user)

class AlbumPostViewSet(ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes =[IsAuthenticated]
    serializer_class =AlbumPostSerializer
    queryset=Album.objects.all()


class FollowUserView(APIView):

    def get(self, request, format=None, username=None):
        to_user = get_user_model().objects.get(username=username)
        from_user = self.request.user
        follow = None
        if from_user.is_authenticated:
            if from_user != to_user:
                if from_user in to_user.followers.all():
                    follow = False
                    from_user.following.remove(to_user)
                    to_user.followers.remove(from_user)
                else:
                    follow = True
                    from_user.following.add(to_user)
                    to_user.followers.add(from_user)
        data = {
            'follow': follow
        }
        return Response(data)
class GetFollowersView(generics.ListAPIView):
    
    serializer_class = FollowSerializer
    
    permission_classes =[IsAuthenticated]


    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(
            username=username).followers.all()
        return queryset


class GetFollowingView(generics.ListAPIView):
    serializer_class = FollowSerializer   
    permission_classes =[IsAuthenticated]


    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(
            username=username).following.all()
        return queryset


# class JoinedEventsView(viewsets.ModelViewSet):
#     serializer_class=JoinedeventsSerializer
#     permission_classes =[IsAuthenticated]
#     queryset=JoinedPeople.objects.all()
#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)



class SendHostView(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class=SendHostSerializers
    queryset =SendHostRequest.objects.all()
    # def perform_create(self,serializer):
    #     serializer.save(user=self.request.user)

class SendHostViewGet(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class=SendHostSerializersGet
    queryset =SendHostRequest.objects.all()

class SendHostReplySerializersPostView(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class=SendHostReplySerializersPost
    queryset =SendHostRequestReply.objects.all()
    # def perform_create(self,serializer):
    #     serializer.save(user=self.request.user)

class SendHostReplySerializersGetView(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class=SendHostSerializersReplyGet
    queryset =SendHostRequestReply.objects.all()
    
class FeedbackView(ModelViewSet):
    serializer_class=FeedbackSerializer
    permission_classes =[IsAuthenticated]
    queryset=Feedback.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class FriendrequestView(ModelViewSet):
    serializer_class=FriendshipRequestSerializer
    permission_classes =[IsAuthenticated]
    queryset=Friendrequest.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


# class Useredit(APIView):
#     def get_object(self, pk):
#         try:
#             return MyUser.objects.get(id=pk)
#         except MyUser.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         print("user : ",user)
#         if user.is_active:
#             user.is_active = False
#         else:
#             user.is_active = True
#         user.save()
#         return Response({"active_status":user.is_active})

class BlockUserView(APIView):
    
    def get_object(self,pk):

        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    def get(self,request,pk,format=None):
        permission_classes =[IsAuthenticated]

        user=self.get_object(pk)
        if user.is_active:
            user.is_active=False
        else:
            user.is_active=True
        user.save()
        return Response({"active status":user.is_active})


# class JoinedEventsView(viewsets.ModelViewSet):
#     serializer_class=JoinedeventsSerializer
#     permission_classes =[IsAuthenticated]
#     queryset=JoinedPeople.objects.all()
#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)
class ReportUserView(ModelViewSet):
    serializer_class=ReportUserGetSerializer
    permission_classes =[IsAuthenticated]
    queryset=ReportUser.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class ReportUserPostView(ModelViewSet):
    serializer_class=ReportUserPostSerializer
    permission_classes =[IsAuthenticated]
    queryset=ReportUser.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class BlockUserGet(ModelViewSet):
    serializer_class=BlockUserGetSerializer
    permission_classes =[IsAuthenticated]
    queryset=User.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


class BlockUserPost(ModelViewSet):
    serializer_class=BlockUserPostSerializer
    permission_classes =[IsAuthenticated]
    queryset=User.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)


# class BlockUserPostView(ModelViewSet):
#     serializer_class=BlockUserPostSerializer
#     permission_classes =[IsAuthenticated]
#     queryset=BlockUser.objects.all()
#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)


# class FriendRequestSend(generics.CreateAPIView):
#     serializer_class=FriendshipRequestSerializer
#     permission_classes =[IsAuthenticated]
#     def get(self,request,request_id=None):
#         friendrequest=get_object_or_404(Friendrequest,pk=request_id)
#         comments_data=self.serializer_class(
#             event.comments,many=True,context={"request":request}
#         ).data

#         return Response(data=comments_data)
#     def post(self,request,event_id=None):
#         event=Event.objects.get(pk=event_id)
#         serializer=CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(event=event,author=self.request.user)
#             return Response(serializer.data,status=status.HTTP_201_NO_CONTENT)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     def delete(self,request,event_id):
#         event=self.get_object(pk=event_id)
#         event.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
class FriendRequestList(APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request,format=None):
        f_requests=Friendrequest.objects.all() 
        serializer=FriendshipRequestGetSerializer(f_requests,many=True) 
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=FriendshipRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class FriendRequestDetail(APIView):
    def get_objects(self,pk):
        try:
            return Friendrequest.objects.get(pk=pk)
        except:
            raise Http404
    def get(self,request,pk,format=None):
        frnd_request=self.get_objects(pk)
        serializer=FriendshipRequestGetSerializer(frnd_request)
        return Response(serializer.data)
    def put(self,request,pk,format=None):
        frnd_request=self.get_objects(pk)
        serializer=FriendshipRequestSerializer(frnd_request,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk,format=None):
        frnd_request =self.get_objects(pk)
        serializer=FriendshipRequestSerializer(frnd_request,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        frnd_request=self.get_objects(pk)
        frnd_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class pop_dest_view(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class=Pop_dest_serializer
    queryset =PopularDest.objects.all()
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

