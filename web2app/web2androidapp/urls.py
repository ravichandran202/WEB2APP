from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name='home'),
    path("login",views.login,name='login'),
    path("signup",views.signup,name='signup'),
    path("profile",views.profile,name='profile'),
    path("upload",views.upload,name='upload'),
    path("download",views.download,name='download'),
]
