
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import datetime
from django.utils.timezone import now
from datetime import date
from django.conf import settings
# Create your models here.


    
class Languages(models.Model):
    language=models.TextField()
class UserManager(BaseUserManager):
    def create_user(self, email,phone_number ,username,first_name, last_name,password=None,repassword=None):
        """
        Creates and saves a User with the given email,phone ,username,first_name, last_name, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password, 
            
           
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email,phone_number ,username,first_name, last_name,password=None):
        """
        Creates and saves a superuser with the given email,phone ,username,first_name, last_name, and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password,  
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


AUTH_PROVIDERS={'google': 'google'}
GENDER=(
    ('Female','Female'),
    ('Male','Male'),
    ('Other','Other')
)
HOSTING_CHOICES = (
    ('Accepting Guests','Accepting Guests'),
    ('Maybe Accepting Guests','Maybe Accepting Guests'),
    ('Not Accepting Guests','Not Accepting Guests')
)
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(max_length=10)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateField(blank=True, null=True,default=datetime.date.today)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255,blank=True,null=True,default=AUTH_PROVIDERS.get('email'))
    dob=models.DateField(max_length=8,null=True,blank=True)
    age=models.IntegerField(null=True, blank=True)
    gender=models.CharField(max_length=10,choices=GENDER,null=True)
    prefered_language=models.CharField(max_length=250,null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to="profilephotos",
        default='avatar.png',null=True,blank=True)
    banner_pic=models.ImageField(upload_to="banner_pic",null=True,blank=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="user_followers",
                                       blank=True,
                                       symmetrical=False,null=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="user_following",
                                       blank=True,
                                       symmetrical=False,null=True)
    hosting_check=models.CharField(max_length=50,choices=HOSTING_CHOICES,default='Maybe Accepting Guests',null=True, blank=True)
    born_location=models.CharField(max_length=50,null=True, blank=True)
    occupation=models.CharField(max_length=50,null=True, blank=True)
    education=models.CharField(max_length=50,null=True, blank=True)
    # languages=models.ForeignKey(Languages,on_delete=models.CASCADE,null=True, blank=True)
    about_me=models.TextField(null=True, blank=True)
    motto=models.TextField(null=True, blank=True)
    interests=models.TextField(null=True, blank=True)
    fav_movies=models.TextField(null=True, blank=True)
    countries_visited=models.TextField(null=True, blank=True)
    countries_lived=models.TextField(null=True, blank=True)
    blocked=models.BooleanField(default=False)
    
    
    objects = UserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number','first_name','last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    def number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0



# HOSTING_CHOICES = (
#     ('Accepting Guests','Accepting Guests'),
#     ('Maybe Accepting Guests','Maybe Accepting Guests'),
#     ('Not Accepting Guests','Not Accepting Guests')
# )


class Country(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    country = models.CharField(max_length=50,null=True)

# class FriendshipRequest(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     created_at=models.DateTimeField(auto_now_add=now, blank=True)

class Album(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="albums")
    image=models.ImageField(upload_to="albums")
    title=models.CharField(max_length=50)
    description=models.TextField()
    created_date=models.DateTimeField(auto_now=True)

# class FriendShipRequest(models.Model):
#     from_user=models.ForeignKey(User,on_delete=models.CASCADE)
#     to_user=models.ForeignKey(User,on_delete=models)
#     message=models.TextField()
#     created

# start_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
#     start_time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
#     end_date=models.DateField(auto_now=False, auto_now_add=False,blank=True, null=True)
#     end_time=models.TimeField(auto_now=False, auto_now_add=False,blank=True, null=True)

class SendHostRequest(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever')
    coming_date=models.DateField(auto_now_add=False)
    coming_time=models.TimeField(auto_now_add=False)
    leaving_date=models.DateField(auto_now_add=False)
    leaving_time=models.TimeField(auto_now_add=False)
    no_travellers=models.IntegerField()
    hostMessage=models.TextField()
    accept=models.BooleanField(default=False)
    decline=models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True,blank=True)
class SendHostRequestReply(models.Model):
    sender=models.ForeignKey(User, related_name="replysender",on_delete=models.CASCADE)
    hostrequest=models.ForeignKey(SendHostRequest,on_delete=models.CASCADE)
    text=models.TextField()


STAYING_SUGGESTION=(
    ('Suggest staying','Suggest Staying'),
    ("Wouldn't Suggest","Wouldn't Suggest")
)

class Feedback(models.Model):
    HostRequest=models.ForeignKey(SendHostRequest,on_delete=models.CASCADE)
    from_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='host')
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='guest')
    feedback_msg=models.TextField()
    suggestion=models.CharField(max_length=50,choices=STAYING_SUGGESTION,default='Suggest staying')

class Friendrequest(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_sender')
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name='request_reciever')
    accept=models.BooleanField(default=False)

REPORTING_REASON=(
    ("It's posting content that shouldn't be here","It's posting content that shouldn't be here"),
    ("It's pretending to be someone else","It's pretending to be someone else"),
)    
class ReportUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='users_reported')
    reporter = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reporter')
    reason=models.CharField(max_length=150,choices=REPORTING_REASON)
    text=models.TextField()


    def __str__(self):
        return self.user.username
# class BlockUser(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocken_user')
#     blocker = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blocked_by')
#     def __str__(self):
#         return self.user.username

class PopularDest(models.Model):
    location=models.CharField(max_length=50)
    pop_image=models.ImageField(upload_to="pop_images",null=True,blank=True)

    
    




    