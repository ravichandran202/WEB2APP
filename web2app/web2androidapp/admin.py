from django.contrib import admin
from .models import AppDetails,Likes,Comments,Reviews
# Register your models here.

@admin.register(AppDetails)
class AdminCreateApp(admin.ModelAdmin):
    list_display = ('user', 'app_name','url')
    
@admin.register(Likes)
class AdminLikes(admin.ModelAdmin):
    list_display = ('user', 'app')
    
@admin.register(Comments)
class AdminComments(admin.ModelAdmin):
    list_display = ('user', 'app')
    
@admin.register(Reviews)
class AdminReviews(admin.ModelAdmin):
    list_display = ('user', 'app','value')