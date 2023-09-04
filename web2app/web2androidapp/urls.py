from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name='home'),
    path("login", views.login, name='login'),
    path("signup", views.signup, name='signup'),
    path("logout", views.logout, name='logout'),
    path("profile/<int:id>", views.profile, name='profile'),
    path("editprofile", views.editProfile, name='editprofile'),
    path("upload", views.upload, name='upload'),
    path("download/<int:id>", views.download, name='download'),
    path("apppage/<int:id>", views.app_page, name='apppage'),
    path("editapp/<int:id>", views.edit_app, name='editapp'),
    path("appstore", views.app_store, name='appstore'),
    path("deleteapp/<int:id>", views.delete_app, name='deleteapp'),
    path("uploadapp/<int:id>", views.upload_app_to_store, name='uploadapp'),

    path("deletecomment/<int:appid>/<int:id>", views.delete_comment, name='deletecomment'),
    path("likeapp/<int:id>", views.like_app, name='likeapp'),
    path("unlikeapp/<int:id>", views.unlike_app, name='unlikeapp'),
]
