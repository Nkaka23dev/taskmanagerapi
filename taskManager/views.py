from django.shortcuts import render
from .models import Project,ClientLocation
from .serializers import ProjectSerializer,ClientLocationSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.filters import SearchFilter 
from django.contrib.auth.models import User 
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer 
    permission_classes=(permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend,SearchFilter] 
    filterset_fields = ['id', 'projectName',] 
    search_fields=['id', 'projectName','DateOfStart','projectSize'] 

class ClientLocationViewSet(viewsets.ModelViewSet):
    queryset=ClientLocation.objects.all() 
    serializer_class=ClientLocationSerializer 
    permission_classes=(permissions.IsAuthenticated,)


