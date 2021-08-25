from rest_framework import serializers 
from .models import User 
from django.contrib import auth 
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer): 
    password=serializers.CharField(max_length=100,min_length=6,write_only=True)

    class Meta:
        model=User
        fields=['email','username','password'] 

    def validate(self,attrs):
        email=attrs.get('email','')
        username=attrs.get('username','')
        

        if not username.isalnum():
            raise serializers.ValidationError("Only alphanumeric characters allowed.") 
        return attrs 

    def create(self,validated_data):
        return User.objects.create_user(**validated_data) 

class EmailVerificationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields=['token'] 

# class LoginSerializer(serializers.ModelSerializer):
#     email=serializers.EmailField(max_length=255)
#     password=serializers.CharField(max_length=100,min_length=6,write_only=True) 
#     username=serializers.CharField(max_length=255,min_length=3,read_only=True)
#     tokens=serializers.CharField(max_length=255,min_length=6,read_only=True)

#     class Meta:
#         model=User
#         fields=['email','password','username','tokens']

#     def validate(self,attrs):
#         email=attrs.get('email','')
#         password=attrs.get('password','')

#         user=auth.authenticate(email=email,password=password) 
#         if not user:
#             raise exceptions.AuthenticationFailed("Invalid credentials, Please try again.") 
#         if not user.is_verified:
#             raise exceptions.AuthenticationFailed("User not verified") 
#         if not user.is_active:
#             raise exceptions.AuthenticationFailed("User not activated.") 
#         return {
#             "email":user.email,
#             "username":user.username,
#             "tokens":user.tokens
#         }

class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD 

class LoginSerializer(EmailTokenObtainSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        if not self.user:
            raise exceptions.AuthenticationFailed("Invalid credentials, Please try again.") 
        if not self.user.is_verified:
            raise exceptions.AuthenticationFailed("User not verified") 
        if not self.user.is_active:
            raise exceptions.AuthenticationFailed("User not activated.")
        data['username'] = self.user.username
        data['email'] = self.user.email 
        data['is_staff']=self.user.is_staff
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token) 
        return data



