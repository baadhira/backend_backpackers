
from django.contrib import admin
from django.urls import path,include
from app.views import *
from app import views 
from rest_framework.routers import DefaultRouter

ROUTER = DefaultRouter()
ROUTER.register("album", AlbumViewSet)
ROUTER.register("albumpost", AlbumPostViewSet)

ROUTER.register("hostrequests", SendHostView)
ROUTER.register("hostrequestsget", SendHostViewGet)

ROUTER.register("sendfeedback", FeedbackView)
ROUTER.register("requesthandler", FriendrequestView)
ROUTER.register("reportuser", ReportUserView)
ROUTER.register("reportuserpost", ReportUserPostView)
ROUTER.register("blockuserget", BlockUserGet)
ROUTER.register("blockuserpost", BlockUserPost)
ROUTER.register("popdest", pop_dest_view)
ROUTER.register("allusers", AllUsers)
ROUTER.register("patchusers", PatchUser)
ROUTER.register("patchprofile", PatchProfile)


ROUTER.register("posthostreply", SendHostReplySerializersPostView)
ROUTER.register("posthostreplyget", SendHostReplySerializersGetView)
# PatchUser

urlpatterns = [
    path("", include(ROUTER.urls)),  
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('userblock/<int:pk>',views.BlockUserView.as_view(),name="userblock"),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('account/<int:pk>/',userAccount.as_view(),name='account'),  
    path('userprofile/<int:pk>/',userProfile.as_view(),name='userprofile'), 
    path('friendrequests/',FriendRequestList.as_view()), 
    path('friendrequest/<int:pk>/',FriendRequestDetail.as_view(),name='friendrequest'),
    path('changepassword/',UserChangePasswordView.as_view(),name='changepassword'),
    path('send-reset-password-email/',SendPasswordRestEmail.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='reset-password'),



    # path('useralbum/<int:pk>/',views.userAlbum.as_view(),name='useralbum'), 
    # path('useralbumcreate/',views.UserAlbumCreate.as_view(),name='useralbumcreate'), 
    # path("album/<album_id>/albumuser",AlbumViewSet.as_view())
]
