from django.db import models  

class ClientLocation(models.Model):
    clientLocationName=models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.clientLocationName}"

class Project(models.Model):
    projectName=models.CharField(max_length=100)
    DateOfStart=models.DateField()
    projectSize=models.IntegerField() 
    active=models.BooleanField(default=False) 
    status=models.CharField(max_length=200)
    clientLocation=models.ForeignKey(ClientLocation,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.projectName}"