from django.urls import path,include
from discussion.views import *
from rest_framework.routers import DefaultRouter
ROUTER = DefaultRouter()
ROUTER.register("discussion", DiscussionViewSet)
ROUTER.register("comment", CommentViewSet)
ROUTER.register("commentpost", CommentPostViewSet)


ROUTER.register("discussioncomments", DiscussionCommentViewSet)
ROUTER.register("likes", LikeViewSet)
ROUTER.register("reportdiscussion", ReportDiscussionViewSet)
ROUTER.register("reportdiscussionpost", ReportDiscussionPostViewSet)
ROUTER.register("replydiscussion", ReplyDiscussion)
ROUTER.register("reportcommentget", ReportCommentGet)
ROUTER.register("reportcommentpost", ReportCommentPost)


ROUTER.register("replydiscussionpost", ReplyDiscussionPost)



urlpatterns = [
    path("", include(ROUTER.urls)),  
    path("discussion/<int:discussion_id>/discussioncomments/",DiscussionComments.as_view()),
    path("liked/", LikedApiView.as_view()),
    path("discussioncomment/<discussioncomment_id>/likes", DiscusssionCommentLikes.as_view()),
    # path("commentlist/", CommentListAPIView.as_view(),name="commentlist"),
    # path("commentcreate/", CommentCreateAPIView.as_view(),name="commentcreate"),

    # path("commentdetail/<int:pk>/", CommentDetailAPIView.as_view(),name="commentdetail"),
]