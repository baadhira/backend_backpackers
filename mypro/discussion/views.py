from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from discussion.models import *
from rest_framework import status
from discussion.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from app.models import *
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
# Create your views here.
class DiscussionViewSet(ModelViewSet):
    # permission_classes =[IsAuthenticated]
    serializer_class =DiscussionSerializer
    queryset=Discussion.objects.all()
    filter_backends =[filters.SearchFilter,DjangoFilterBackend]
    filterset_fields =["author__id","location","question","topic"]
    search_fields =["description","topic","location",'question']

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

        
class DiscussionCommentViewSet(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =DiscussionCommentSerializer
    queryset=DiscussionComment.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class ReplyDiscussion(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =DiscussionReplyCommentSerializer
    queryset=ReplyDiscussionComment.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class ReplyDiscussionPost(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =DiscussionReplyPostCommentSerializer
    queryset=ReplyDiscussionComment.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)


class ReportDiscussionViewSet(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =ReportDiscussionGetSerialzer
    queryset=ReportDiscussion.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
class ReportDiscussionPostViewSet(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =ReportDiscussionPostSerializer
    queryset=ReportDiscussion.objects.all()

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)
class ReportCommentGet(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =ReportCommentGetSerializer
    queryset=ReportComment.objects.all()

    # def perform_create(self,serializer):
    #     serializer.save(author=self.request.user)

class ReportCommentPost(ModelViewSet):
    permission_classes =[IsAuthenticated]
    serializer_class =ReportCommentPostSerializer
    queryset=ReportComment.objects.all()


    
class DiscussionComments(APIView):
    serializer_class=DiscussionCommentSerializer
    def get(self,request,discussion_id):
        discuss=get_object_or_404(Discussion,pk=discussion_id)
        comments_data=self.serializer_class(
            discuss.discussion_comments,many=True,context={"request":request}
        ).data

        return Response(data=comments_data)
    def post(self,request,discussion_id):
        return Response("hiiii")



class LikeViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LikeDisCommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("user__id",)
    queryset = LikeDisComment.objects.all()

    def create(self, request, *args, **kwargs):
        discussioncomment_id = request.data["discussioncomment"]
        discussioncomment = get_object_or_404(DiscussionComment, pk=discussioncomment_id)
        new_like, _ = LikeDisComment.objects.get_or_create(user=request.user, discussioncomment=discussioncomment)
        serializer = self.serializer_class(new_like).data
        return Response(data=serializer,status=status.HTTP_201_CREATED)
        
class LikedApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiscussionCommentSerializer

    def get(self, request):
        liked_discussions = DiscussionComment.objects.filter(likes__author__id=request.user.id)
        serializer_data = self.serializer_class(
            liked_discussions, many=True, context={"request": request}
        ).data

        return Response(data=serializer_data)

class DiscusssionCommentLikes(APIView):
    serializer_class = LikeDisCommentSerializer

    def get(self, request, discussioncomment_id):
        discussioncomment = get_object_or_404(DiscussionComment, pk=discussioncomment_id)
        discussioncomment_data = DiscussionCommentSerializer(discussioncomment, context={"request": request}).data
        likes_data = self.serializer_class(
            discussioncomment.likes, many=True, context={"request": request}
        ).data

        return Response(data={"likes": likes_data, "is_liked": discussioncomment_data["is_liked"]})

# class CommentCreateAPIView(ModelViewSet):
    
#     permission_classes =[IsAuthenticated]
#     serializer_class =CommentPostSerializer

#     queryset=Comment.objects.all()

#     def perform_create(self,serializer):
#         serializer.save(author=self.request.user)



# class CommentDetailAPIView(RetrieveAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetailSerializer
#     lookup_field='pk'

# class CommentListAPIView(ListAPIView):
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]
#     filter_backends= [SearchFilter, OrderingFilter]
#     search_fields = ['content', 'user__first_name']
#     # pagination_class = PostPageNumberPagination #PageNumberPagination

#     def get_queryset(self, *args, **kwargs):
#         #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
#         queryset_list = Comment.objects.filter(id__gte=0) #filter(user=self.request.user)
#         query = self.request.GET.get("q")
#         if query:
#             queryset_list = queryset_list.filter(
#                     Q(content__icontains=query)|
#                     Q(user__first_name__icontains=query) |
#                     Q(user__last_name__icontains=query)
#                     ).distinct()
#         return queryset_list


class CommentViewSet(ModelViewSet):
   
    permission_classes =[IsAuthenticated]
    queryset = Comment.objects.all()
    
    serializer_class = CommentSerializer

    @action(detail=False)
    def roots(self, request):
        queryset = Comment.objects.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CommentPostViewSet(ModelViewSet):
   
    permission_classes =[IsAuthenticated]
    queryset = Comment.objects.all()
    
    serializer_class = CommentPostSerializer

    @action(detail=False)
    def roots(self, request):
        queryset = Comment.objects.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        