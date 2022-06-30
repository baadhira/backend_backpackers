from django.contrib.contenttypes.models import ContentType
from asyncore import read
from rest_framework import serializers
from app.serializers import *
from discussion.models import *
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )
class DiscussionAuthorSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model=User
        fields=['id', 'username','email','profile']
        depth=1

        extra_kwargs={"profile":{'read_only':True}}

class LikeDisCommentSerializer(serializers.ModelSerializer):
    user=DiscussionAuthorSerializer(read_only=True)
    class Meta:
        model=LikeDisComment
        fields="__all__"
        extra_kwargs={"user":{'read_only':True},
            "discussion_comment":{'read_only':True}
        }
class DiscussionCommentSerializer(serializers.ModelSerializer):
    author=DiscussionAuthorSerializer(read_only=True)
    like=LikeDisCommentSerializer(many=True,read_only=True)
    like_amount=serializers.SerializerMethodField("get_like_amount")
    class Meta:
        model=DiscussionComment
        fields=('id','author','discussion','text','like','like_amount')
        extra_kwargs={"author":{'read_only':True}}
    @staticmethod
    def get_like_amount(obj):
        return obj.likes.count()

class DiscussionReplyCommentSerializer(serializers.ModelSerializer):
    author=DiscussionAuthorSerializer(read_only=True)
    discussion_reply=DiscussionCommentSerializer(read_only=True)
    class Meta:
        model=ReplyDiscussionComment
        fields="__all__"
        extra_kwargs={"author":{'read_only':True},
            "discussion_reply":{'read_only':True}
        }

class DiscussionReplyPostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReplyDiscussionComment
        fields=('id','discussion_reply','text')
        




class DiscussionSerializer(serializers.ModelSerializer):
    # comment=DiscussionCommentSerializer(many=True,read_only=True)
    # comments_amount=serializers.SerializerMethodField("get_comments_amount")
    comments=SerializerMethodField()
    
    
    author=DiscussionAuthorSerializer(read_only=True)
    class Meta:
        model=Discussion
        fields=['id','author','location','question','topic','createddate','comments']
        depth=1
        extra_kwargs={
            "author":{'read_only':True},
        }
    @staticmethod
    def get_comments_amount(obj):
        return obj.discussion_comments.count()
    def get_comments(self,obj):
        # content_type=obj.get_content_type
        # object_id=obj.id
        # c_qs=Comment.objects.filter_by_instance(obj)
        # comments=CommentSerializer(c_qs,many=True).data
        # return comments
        pass



class ReportDiscussionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReportDiscussion
        fields=('id','author','discussion','reason','text')
class ReportDiscussionGetSerialzer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    discussion=DiscussionSerializer(read_only=True)
    class Meta:
        model=ReportDiscussion
        fields=('id','author','discussion','reason','text')

# def create_comment_serializer(model_type='discussion',object_id=None,slug=None,parent_id=None,user=None):
#     class CommentCreateSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Comment
#             fields=['id','content','timestamp','object_id']
#     def __init__(self,*args,**kwargs):
#         self.model_type=model_type
#         self.slug=slug
#         self.parent_obj=None
#         if parent_id:
#             parent_qs=Comment.objects.filter(id=parent_id)
#             if parent_qs.exists() and parent_qs.count() == 1:
#                 self.parent_obj=parent_qs.first()
#         return super(CommentCreateSerializer,self).__init__(*args,**kwargs)

#     def validate(self,data):
#         model_type=self.model_type
#         model_qs=ContentType.objects.filter(model=model_type)
#         if not model_qs.exists() or model_qs.count != 1:
#             raise ValidationError("This is not a valid content type")
#         SomeModel = model_qs.first().model_class()
#         obj_qs=SomeModel.objects.filter(slug=self.slug)
#         if not obj_qs.exists() or obj_qs.count != 1:
#             raise ValidationError("This is not a slug for this content type")
#         return data
#     def create(self,validated_data):
#         content=validated_data.get("content")
#         if user:
#             main_user=user
#         else:
#             main_user=User.objects.all().first()
        
#         model_type=self.model_type
#         slug=self.slug
#         parent_obj=self.parent_obj
#         comment=Comment.objects.create_by_model_type(
#             model_type,
#             main_user,
#             content,
#             parent_obj=parent_obj

#             )
#         return comment
#     return CommentCreateSerializer
# class CommentSerializer(serializers.ModelSerializer):
#     reply_count=SerializerMethodField()
#     class Meta:
#         model=Comment
#         fields=['id', 'content_type','object_id','parent','content','reply_count','timestamp']
#     def get_reply_count(self,obj):
#         if obj.is_parent:
#             return obj.children().count()
#         return 0

# class CommentPostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Comment
#         fields=['id', 'content_type','object_id','parent','content']
#     def get_reply_count(self,obj):
#         if obj.is_parent:
#             return obj.children().count()
#         return 0
    


# class CommentChildSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Comment
#         fields=['id', 'content','timestamp']
    
# class CommentPostSerializer(serializers.ModelSerializer):
#     user=DiscussionAuthorSerializer(read_only=True)
#     like=LikeDisCommentSerializer(many=True,read_only=True)
#     like_amount=serializers.SerializerMethodField("get_like_amount")
#     class Meta:
#         model=DiscussionComment
#         fields=('id','user','discussion','text','content','timestamp','like','like_amount')
#         extra_kwargs={"author":{'read_only':True}}
#     @staticmethod
#     def get_like_amount(obj):
#         return obj.likes.count()


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    reply_set = RecursiveSerializer(many=True, read_only=True)
    user=DiscussionAuthorSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','user', 'date', 'comment', 'from_discussion', 'parent', 'reply_set')

class CommentPostSerializer(serializers.ModelSerializer):
    reply_set = RecursiveSerializer(many=True, read_only=True)
  
    class Meta:
        model = Comment
        fields = ('id','user', 'date', 'comment', 'from_discussion', 'parent', 'reply_set')

class ReportCommentGetSerializer(serializers.ModelSerializer):
    comment=CommentSerializer(read_only=True)

    class Meta:
        model=ReportComment
        fields=('id','reporter','comment','date','reason')


class ReportCommentPostSerializer(serializers.ModelSerializer):
 
    class Meta:
        model=ReportComment
        fields=('id','reporter','comment','date','reason')