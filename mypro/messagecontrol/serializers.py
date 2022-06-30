from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import GenericFileUpload,MessageAttachment,Message

class GenericFileUploadSerializer(ModelSerializer):
    class Meta:
        model = GenericFileUpload
        fields = '__all__'


class MessageAttachmentSerializer(serializers.ModelSerializer):
    attachment = GenericFileUploadSerializer()

    class Meta:
        model = MessageAttachment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField("get_sender_data")
    sender_id = serializers.IntegerField(write_only=True)
    receiver = serializers.SerializerMethodField("get_receiver_data")
    receiver_id = serializers.IntegerField(write_only=True)
    message_attachments = MessageAttachmentSerializer(
        read_only=True, many=True)

    class Meta:
        model = Message
        fields = "__all__"

    def get_receiver_data(self, obj):
        from app.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.receiver).data

    def get_sender_data(self, obj):
        from app.serializers import UserProfileSerializer
        return UserProfileSerializer(obj.sender).data