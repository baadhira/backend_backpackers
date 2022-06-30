from django.db import models
from app.models import User
# Create your models here.

class ConversationModel(models.Model):
    user1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1')
    user2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user2')
