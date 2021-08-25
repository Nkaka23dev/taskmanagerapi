from django.shortcuts import render
from rest_framework import generics,status,views 
from .serializers import RegisterSerializer,EmailVerificationSerializer,LoginSerializer
from rest_framework.response import Response 
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .utils import Utils 
from .models import User 
from django.conf import settings
import jwt 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data=serializer.data
        user=User.objects.get(email=user_data['email']) 
        token=RefreshToken().for_user(user).access_token
        relativeLink=reverse('verify-email')
        current_domain=get_current_site(request).domain
        absurl="http://"+current_domain+relativeLink+"?token="+str(token)
        email_body="Hi,"+user.username+" Use the link below to verify your email \n"+absurl
        data={'email_body':email_body,'email_subject':'Verify Email',
        'to_user':user.email}

        Utils.send_email(data)
        return Response(
        {
            'data':user_data,
        }
        ,status=status.HTTP_201_CREATED
        )
    
class VerifyEmail(views.APIView):
    serializer_class=EmailVerificationSerializer
    token_params_config=openapi.Parameter('token',in_=openapi.IN_QUERY,description="desc",
    type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_params_config])
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token, settings.SECRET_KEY,algorithms='HS256')
            user=User.objects.get(id=payload['user_id']) 
            if not user.is_verified: 
                user.is_verified=True 
                user.save()
            return Response(
                {'Email':'Email successfull activated'},status=status.HTTP_200_OK
            ) 
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'Error':'Activation expired'},status=status.HTTP_400_BAD_REQUEST
            ) 
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {'Error':'Invalid Token'},status=status.HTTP_400_BAD_REQUEST
            )  

class LoginView(TokenObtainPairView):
    serializer_class=LoginSerializer 
    # def post(self,request):
    #     serializer=self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user_data=serializer.data
    #     return Response({
    #        'data':serializer.data 
    #     },status=status.HTTP_200_OK)