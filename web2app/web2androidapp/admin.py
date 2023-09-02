from django.contrib import admin
from .models import AppDetails
# Register your models here.

@admin.register(AppDetails)
class AdminCreateApp(admin.ModelAdmin):
    list_display = ('user', 'app_name','url')