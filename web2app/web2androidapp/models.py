from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class BasicInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class UserBasicInfo(BasicInfo):
    user =  models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile',blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    first_name = models.CharField(max_length=100,blank=True,null=True)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True)
    position = models.CharField(max_length=100,blank=True,null=True)
    about = models.CharField(max_length=10000,blank=True,null=True)
    website = models.URLField(blank=True,null=True)
    
    def __str__(self):
        return str(self.first_name) + str(self.last_name)

class AppDetails(BasicInfo):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    app_image = models.ImageField(upload_to='appimages',blank=True,null=True)
    app_name = models.CharField(max_length=20)
    about = models.CharField(max_length=10000,blank=True,null=True) 
    url = models.URLField()
    is_upload = models.BooleanField(default=False)
    total_downloads = models.IntegerField(default=0)
    def __str__(self):
        return str(self.app_name)
    
class Likes(BasicInfo):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    app = models.ForeignKey(AppDetails,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user) + " " + str(self.app)
    
class Comments(BasicInfo):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    app = models.ForeignKey(AppDetails,on_delete=models.CASCADE)
    content =  models.CharField(max_length=100000, blank=False)
    
    def __str__(self):
        return str(self.user) + " " + str(self.app)

    