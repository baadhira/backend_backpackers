
# from django.contrib import admin
from django.urls import path,include
from event.views import *
from rest_framework.routers import DefaultRouter
from event import views
ROUTER = DefaultRouter()
ROUTER.register("events", EventViewSet)
ROUTER.register("comments", CommentViewSet)
ROUTER.register("joinedusers", JoinedEventsView)
ROUTER.register("getjoinedusers", GetJoinedEventsView)
ROUTER.register("reportevent", ReportEvent)
ROUTER.register("reporteventpost", ReportEventPost)
ROUTER.register("eventcomment", EventCommentViewSet)
ROUTER.register("eventcommentpost", EventCommentPostViewSet)


# ROUTER.register("comments", CommentViewSet)
urlpatterns = [
    path("", include(ROUTER.urls)),  
    path("events/<event_id>/comments",EventComments.as_view()),
    # path('eventjoin/<int:id>/',views.JoinView.as_view(),name='eventjoin'),
]
