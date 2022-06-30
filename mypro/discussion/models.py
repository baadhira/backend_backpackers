from __future__ import unicode_literals

from django.db import models
from app.models import *
from django.utils.timezone import now
import datetime

class Discussion(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='discussions')
    location=models.CharField(max_length=100)
    question=models.TextField()
    topic=models.CharField(max_length=50)
    # created_date = models.DateTimeField(blank=True, null=True,default=now,editable=True)
    createddate=models.DateField(blank=True, null=True,default=datetime.date.today)
    
    def __str__(self):
        return f"Question asked by {self.author.username}"
    class Meta:
        ordering =["-createddate"]
    
    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

class DiscussionComment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE,related_name="discussion_comments")
    text=models.CharField(max_length=255)
    def __str__(self):
        return f"Answered by {self.author.username}"

class LikeDisComment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    discussion_comment=models.ForeignKey(DiscussionComment,on_delete=models.CASCADE,related_name="likes")
    def __str__(self):
        return f"Like from {self.user} to {self.discussion_comment}"

class ReplyDiscussionComment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    discussion_reply = models.ForeignKey(DiscussionComment, on_delete=models.CASCADE,related_name="discussion_comments")
    text=models.CharField(max_length=255)
    def __str__(self):
        return f"Answered by {self.author.username}"

REPORTING_REASON=(
    ("It's spam","It's spam"),
    ("Hate speech or symbols","Hate speech or symbols"),
    ("Bullying or harassement","Bullying or harassement"),
    ("Nudity or sexual activity","Nudity or sexual activity"),

) 
class ReportDiscussion(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    reason=models.CharField(max_length=150,choices=REPORTING_REASON)
    text=models.TextField()


from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models

class CommentManager(models.Manager):
    def all(self):
        qs=super(CommentManager, self).filter(parent=None)
        return qs 
    def filter_by_instance(self, instance):
        content_type =ContentType.objects.get_for_model(instance.__class__)
        obj_id=instance.id
        qs=super(CommentManager, self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
        return qs
    def create_by_model_type(self,model_type,content,slug,user,parent_obj=None):
        model_qs=ContentType.objects.filterr(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs=SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count == 1:
                instance=self.model()
                instance.content=content  
                instance.user=user
                instance.content_type=model_qs.first()
                instance.object_id=obj_qs.first().id
                if parent_obj:
                    instance.parent=parent_obj
                instance.save()
                return instance
        return None


# class Comment(models.Model):
#     user        = models.ForeignKey(User, default=1,on_delete=models.CASCADE,related_name='usercomment')
#     # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     discussion = models.ForeignKey(Discussion,on_delete=models.CASCADE,related_name='discussion_id')
    
#     parent      = models.ForeignKey("self",on_delete=models.CASCADE, null=True, blank=True,related_name="parentcomment")

#     content     = models.TextField()
#     timestamp   = models.DateTimeField(auto_now_add=True)

#     objects = CommentManager()

#     class Meta:
#         ordering = ['-timestamp']


#     def __unicode__(self):  
#         return str(self.user.username)

#     def __str__(self):
#         return str(self.user.username)

#     def get_absolute_url(self):
#         return reverse("comments:thread", kwargs={"id": self.id})

#     def get_delete_url(self):
#         return reverse("comments:delete", kwargs={"id": self.id})
        
#     def children(self): #replies
#         return Comment.objects.filter(parent=self)

#     @property
#     def is_parent(self):
#         if self.parent is not None:
#             return False
#         return True



    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commenter")
    comment = models.CharField(max_length=250)
    from_discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='from_discussion')
    parent = models.ForeignKey('self', related_name='reply_set', null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
REPORTING_REASON=(
    ("It's spam","It's spam"),
    ("Hate speech or symbols","Hate speech or symbols"),
    ("Bullying or harassement","Bullying or harassement"),
    ("Nudity or sexual activity","Nudity or sexual activity"),

) 
class ReportComment(models.Model):
    reporter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_reporter')
    reason=models.CharField(max_length=150,choices=REPORTING_REASON)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='reported_comment')
    date = models.DateTimeField(auto_now=True)

