from django.db import models
from app.models import *
from django.utils.timezone import now

class Event(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="events") 
    event_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="events",blank=True, null=True)
    location=models.CharField(max_length=100)
    # startdate_time=models.DateTimeField(blank=True, null=True)
    # enddate_time=models.DateTimeField(blank=True, null=True)
    start_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    start_time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    end_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
    end_time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    limit_attendees = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True,default=now,editable=True)
    
    # joiners = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #                                    related_name="users_joining",
    #                                    blank=True,
    #                                    symmetrical=False,null=True)
    # joiners = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #                                related_name="joiners",
    #                                blank=True,
    #                                symmetrical=False)
    
    # def number_of_joiners(self):
    #     if self.joiners.count():
    #         return self.joiners.count()
    #     else:
    #         return 0
    
    def __str__(self):
        return f"{self.event_name}"
    class Meta:
        ordering =["-created_date"]
    

    

class JoinedPeople(models.Model):
    event= models.ForeignKey(Event,on_delete=models.CASCADE)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.event.event_name}"


class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    events = models.ForeignKey(Event, on_delete=models.CASCADE,related_name="comments")
    text=models.CharField(max_length=255,null=True)
    def __str__(self):
        return f"{self.text}"
REPORTING_REASON=(
    ("It's spam","It's spam"),
    ("Hate speech or symbols","Hate speech or symbols"),
    ("Bullying or harassement","Bullying or harassement"),
    ("Nudity or sexual activity","Nudity or sexual activity"),

) 
class ReportEvent(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reported_by")
    event =models.ForeignKey(Event,on_delete=models.CASCADE)
    reason=models.CharField(max_length=150,choices=REPORTING_REASON)
    text=models.TextField()

  
class EventComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="eventcommenter")
    comment = models.CharField(max_length=250)
    from_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='from_event')
    parent = models.ForeignKey('self', related_name='reply_set', null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)







