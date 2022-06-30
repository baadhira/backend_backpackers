from rest_framework import serializers
from app.models import User,Album,SendHostRequest,Feedback,Friendrequest,ReportUser,PopularDest,SendHostRequestReply 
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from friendship.models import FriendshipRequest
from django.contrib.auth import get_user_model

from app.utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
    repassword=serializers.CharField(style={"input_type":'password'},write_only=True)

    class Meta:
        model = User
        fields=['email','phone_number' ,'username','first_name', 'last_name', 'password', 'repassword']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password =attrs.get('password')
        repassword =attrs.get('repassword')
        if password != repassword:
            raise serializers.ValidationError("passwords doesn't match")
        return attrs

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=50)
    class Meta:
        model = User
        fields = ['username','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','phone_number' ,'first_name', 'last_name',]

class UserchangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    repassword=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    
    class Meta:
        fields=['password', 'repassword']
    def validate(self,attrs):
        password=attrs.get('password')
        repassword=attrs.get('repassword')
        user=self.context.get('user')
        if password != repassword:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    
    def validate(self,attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('encoded uid',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('password reset link',link)
            # send email
            body='Click Following Link To Reset Your Password'+link
            data={
                "subject":'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationError('You are not a registered user')
        # return super().validate(attrs)
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    repassword=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    
    class Meta:
        fields=['password', 'repassword']
    def validate(self,attrs):
        try:
            password=attrs.get('password')
            repassword=attrs.get('repassword')
            uid=self.context.get('uid')
            token=self.context.get('token')

            if password != repassword:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('token is not valid or expired')
                
            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('token is not valid or expired')






class Accountserializer(serializers.ModelSerializer):
    class Meta:
        model=User 
        fields=['id','username','email','phone_number' ,'first_name', 'last_name','dob','age','gender','prefered_language','address','blocked']

class ProfileSerializer(serializers.ModelSerializer):
    # followed_by_req_user = serializers.SerializerMethodField()
    userone=UserProfileSerializer(many=True,read_only=True)  
    class Meta:
        model = User
        fields=['id','userone','username','hosting_check','first_name', 'last_name','born_location','occupation','education','prefered_language','about_me','motto','interests','fav_movies','countries_visited','countries_lived']
        depth=1

        extra_kwargs={"userone":{'read_only':True}}


    # def get_followed_by_req_user(self, obj):
    #     user = self.context['request'].user
    #     return user in obj.followers.all()

class FollowSerializer(serializers.ModelSerializer):
    """Serializer for listing all followers"""

    class Meta:
        model = get_user_model()
        fields = ('username')



class UserSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer(read_only=True)
    class Meta:
        model=User
        fields=['id', 'username','email','profile','blocked']
        depth=1

        extra_kwargs={"profile":{'read_only':True}}

class UserList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','is_active','is_admin','created_at','phone_number','blocked','born_location','hosting_check']    



class AlbumSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=Album
        fields=['id','user','image','title','description','created_date']
        depth=1
        extra_kwargs={
            "author":{'read_only':True},
        }

class AlbumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Album
        fields=['id','user','image','title','description','created_date']
      
   
        

class SendHostSerializers(serializers.ModelSerializer):
    # from_user=UserSerializer(read_only=True)
    # to_user=UserSerializer(read_only=True)
    class Meta:
        model = SendHostRequest
        fields = ['id','from_user','coming_date','coming_time','created_date','no_travellers','leaving_date','leaving_time','to_user','hostMessage','accept','decline']


class SendHostSerializersGet(serializers.ModelSerializer):
    from_user=ProfileSerializer(read_only=True)
    to_user=ProfileSerializer(read_only=True)

    class Meta:
        model = SendHostRequest
        fields = ['id','from_user','coming_date','coming_time','created_date','no_travellers','leaving_date','leaving_time','to_user','hostMessage','accept','decline']
class SendHostReplySerializersPost(serializers.ModelSerializer):
    # sender=ProfileSerializer(read_only=True)
    # hostrequest=SendHostSerializers(read_only=True)

    class Meta:
        model = SendHostRequestReply
        fields = ['id','sender','hostrequest','text']


class SendHostSerializersReplyGet(serializers.ModelSerializer):
    sender=ProfileSerializer(read_only=True)
    hostrequest=SendHostSerializers(read_only=True)

    class Meta:
        model = SendHostRequestReply
        fields = ['id','sender','hostrequest','text']
# SendHostRequestReply
class FeedbackSerializer(serializers.ModelSerializer):
    from_user=UserSerializer(read_only=True)
    to_user=UserSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields=('id', 'from_user','to_user','feedback_msg','suggestion')

class FriendshipRequestSerializer(serializers.ModelSerializer):
    # sender=UserSerializer(read_only=True)
    # reciever=UserSerializer(read_only=True)
    class Meta:
        model=Friendrequest
        fields=('id','sender','reciever','accept')
    # @staticmethod
    # def get_friends_list(obj):
    #     return obj.reciever.count()
class FriendshipRequestGetSerializer(serializers.ModelSerializer):
    sender=UserSerializer(read_only=True)
    reciever=UserSerializer(read_only=True)
    # requests_amount=serializers.SerializerMethodField("get_friends_list")

    class Meta:
        model=Friendrequest
        fields=('id','sender','reciever','accept')  
    # ,'requests_amount'
    # @staticmethod
    # def get_friends_list(obj):
    #     return obj.request_sender.count()
class ReportUserGetSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    reporter=UserSerializer(read_only=True)
    class Meta:
        model=ReportUser
        fields=('id',"user",'reporter','reason','text')
class ReportUserPostSerializer(serializers.ModelSerializer):
    # user=UserSerializer(read_only=True)
    # reporter=UserSerializer(read_only=True)
    class Meta:
        model=ReportUser
        fields=('id',"user",'reporter','reason','text')

class BlockUserGetSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model=User
        fields=('id',"user",'is_active')
class BlockUserPostSerializer(serializers.ModelSerializer):
    # user=UserSerializer(read_only=True)
    class Meta:
        model=User
        fields=('id',"user",'is_active')


class Pop_dest_serializer(serializers.ModelSerializer):
    class Meta:
        model=PopularDest
        fields=('id','location','pop_image')