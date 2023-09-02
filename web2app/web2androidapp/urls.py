from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name='home'),
    path("login",views.login,name='login'),
    path("signup",views.signup,name='signup'),
    path("logout",views.logout,name='logout'),
    path("profile",views.profile,name='profile'),
    path("upload",views.upload,name='upload'),
    path("download/<int:id>",views.download,name='download'),
    path("apppage/<int:id>",views.app_page,name='apppage'),
    path("appstore",views.app_store,name='appstore'),
]