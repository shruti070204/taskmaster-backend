from rest_framework import serializers #DRF module provides tools to serialize/deserialize data
from .models import Task,Priority,AuditLog
from django.contrib.auth.models import User #builtin User model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #base class for custom jwt token content
#serialize all fields of priority, they can be read and write via API
class PrioritySerializers(serializers.ModelSerializer): #auto genetrate model fields
    class Meta:
        model= Priority
        fields='__all__' #include all field of model

#allows whom to assign the task
class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model= Task
        fields='__all__'
        extra_kwargs = {
            'assigned_to':{'required': False}, #prompts to drf: if field missing from incoming json dont raise err
    }
# used in sdmin audit log API view(AuditLogViewSet) 
class AuditLogSerializers(serializers.ModelSerializer):
    class Meta:
        model= AuditLog
        fields='__all__'

#display minimal user data
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username','email'] #not all coz to hide sensitive data as pwd,is_staff

class RegisterationSerializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True) #password accepted in post data not received in get data
    is_staff = serializers.BooleanField(default=False) # lets frontens optionally register an admin(true) or just user(false)

    class Meta:
        model=User
        fields=['username','email','password','is_staff'] #only fields exposed in registeration API
        extra_kwargs={'password': {'write_only':True}} #agaon confirm pwd is write only

#handles user creation with password encryption
    def create(self, validated_data):
        user=User.objects.create_user( #handle pwd hashing
            username=validated_data['username'],
            email=validated_data['email'],
            is_staff=validated_data.get('is_staff', False),
        )
        user.set_password(validated_data['password']) #explicitly hashes
        user.save() #called auto when this is used
        return user 
#add is_staff and user to jwt payload
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer): #Extends the default JWT serializer to add custom data into the token payload.
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) #genrate jwt token
        token['username'] = user.username #frontend used to greet user
        token['is_staff'] = user.is_staff #frontend show/hide admin features
        return token