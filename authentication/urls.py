from django.urls import path 
from .views import RegisterView,VerifyEmail,LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('register/',RegisterView.as_view(),name="register-view"),
    path('verify-email/',VerifyEmail.as_view(),name="verify-email"),
    path('login/',LoginView.as_view(),name="login-view"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]