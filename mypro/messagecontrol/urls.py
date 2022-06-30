from rest_framework.routers import DefaultRouter
from .views import  GenericFileUploadViewSet,MessageView
from django.urls import path,include
router=DefaultRouter(trailing_slash=False)

router.register('fileupload', GenericFileUploadViewSet)
router.register('message', MessageView)


urlpatterns=[
    path('',include(router.urls))
]