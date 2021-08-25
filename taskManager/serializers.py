from rest_framework import serializers
from .models import Project,ClientLocation
from django.contrib.auth.models import User 

class ClientLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=ClientLocation 
        fields=['url','id','clientLocationName']
 
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ['url', 'id', 'projectName', 'DateOfStart','projectSize','active','status','clientLocation'] 

