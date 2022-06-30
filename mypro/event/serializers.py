from rest_framework import serializers
from event.models import *
from app.serializers import *
from django.contrib.auth import get_user_model
# class CommentSerializer(serializers.ModelSerializer):
#     reply_count=serializers.SerializerMethodField()
#     user =serializers.SerializerMethodField() 
#     class Meta:
#         model=addComment
#         fields=('id','content','parent','user','reply_count','event')  
#         def get_reply_count(self,obj):
#             if obj.is_parent:
#                 return obj.children().count()
#             return 0
#         def ger_user(self,obj):
#             return obj.user.username
class AuthorSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model=User
        fields=['id', 'username','email','profile']
        depth=1

        extra_kwargs={"profile":{'read_only':True}}


class CommentSerializer(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    class Meta:
        model=Comment
        fields="__all__"
        extra_kwargs={"author":{'read_only':True}}



class EventSerializer(serializers.ModelSerializer):
    comment=CommentSerializer(many=True,read_only=True)
    comments_amount=serializers.SerializerMethodField("get_comments_amount")
    # join_req_user=serializers.SerializerMethodField()
    author=ProfileSerializer(read_only=True)
    # image=serializers.ImageField(write_only=True)
    # joined_by_req_user = serializers.SerializerMethodField()
    class Meta:
        model=Event
        fields=['id','author','event_name','image','location','start_date','start_time','end_date','end_time','limit_attendees','description','created_date','comment','comments_amount']
        depth=1
        extra_kwargs={
            "author":{'read_only':True},
        }
    @staticmethod
    def get_comments_amount(obj):
        return obj.comments.count()
    # ,'joined_by_req_user'
    # def get_joined_by_req_user(self, obj):
    #     user = self.context['request'].user
    #     return user in obj.joiners.all()

# class EventSerializer(serializers.ModelSerializer):
#     user=serializers.SerializerMethodField()
    

#     class Meta:
#         model=Event
#         fields =('id','author','image','limit_attendees','startdate_time','enddate_time','event_name','location','description','created_date')
    
#     def get_user(self,obj):
#         return obj.user.username
class JoinedeventsSerializer(serializers.ModelSerializer):
    # user=AuthorSerializer(read_only=True)
    # event=EventSerializer(read_only=True)
    class Meta:
        model=JoinedPeople
        fields=('id','user','event')

class GetJoinedeventsSerializer(serializers.ModelSerializer):
    user=AuthorSerializer(read_only=True)
    event=EventSerializer(read_only=True)
    class Meta:
        model=JoinedPeople
        fields=('id','user','event')

    # class Meta:
    #     model =JoinedPeople
    #     fields=('event','user')


# class JoinersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Event
#         fields=('username')
class EventReportSerializerGet(serializers.ModelSerializer):
    author=AuthorSerializer(read_only=True)
    event=EventSerializer(read_only=True)
    class Meta:
        model=ReportEvent
        fields=('id','author','event','reason','text')
class EventReportSerializerPost(serializers.ModelSerializer):
    class Meta:
        model=ReportEvent
        fields=('id','author','event','reason','text')




class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class EventCommentSerializer(serializers.ModelSerializer):
    reply_set = RecursiveSerializer(many=True, read_only=True)
    user=AuthorSerializer(read_only=True)
    class Meta:
        model = EventComment
        fields = ('id','user', 'date', 'comment', 'from_event', 'parent', 'reply_set')

class EventCommentPostSerializer(serializers.ModelSerializer):
    reply_set = RecursiveSerializer(many=True, read_only=True)
  
    class Meta:
        model = EventComment
        fields = ('id','user', 'date', 'comment', 'from_event', 'parent', 'reply_set')



