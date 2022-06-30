from rest_framework import serializers
from .models import *
from app.serializers import *
from app.models import User

class ConversationSerializer(serializers.ModelSerializer):
    user1=UserSerializer()
    user2=UserSerializer()

    class Meta:
        model = ConversationModel
        fields ="__all__"
