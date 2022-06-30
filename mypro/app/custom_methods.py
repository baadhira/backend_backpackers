from rest_framework.permissions import BasePermission,SAFE_METHODS
from django.utils import timezone
from rest_framework.views import exception_handler
from rest_framework.response import Response

class IsAuthenticatedCustom(BasePermission):
    def has_permission(self,request,view):
        if request.user and request.user.is_authenticated:
            from app.models import User

            return True
        return False

class IsAuthenticatedReadCustom(BasePermission):
    def has_permission(self,request,view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            from app.models import User

            return True
        return False

def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        return response

    exc_list = str(exc).split("DETAIL: ")

    return Response({"error": exc_list[-1]}, status=403)