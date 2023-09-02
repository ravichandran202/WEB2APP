from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BasicInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AppDetails(BasicInfo):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    app_image = models.ImageField(upload_to='appimages',blank=True,null=True)
    app_name = models.CharField(max_length=20)
    url = models.URLField()
    
    def __str__(self):
        return str(self.app_name)