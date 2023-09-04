from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import shutil
import os

from .models import UserBasicInfo,AppDetails,Likes,Comments
from .forms import AppDetailsForm,UserBasicInfoForm
# BASE_DIR = Path(__file__).resolve().parent.parent

def web2app_converter(app_name, url):
    file_path = os.path.join(os.path.dirname(
        __file__), 'AITextApp/app/src/main/java/com/example/aitextapp', 'MainActivity.java')
    content_file_path = os.path.join(os.path.dirname(__file__), 'content.txt')
    zip_folder_path = os.path.join(os.path.dirname(__file__), 'AITextApp')
    android_code_file = open(file_path, 'w')
    get_code_file = open(content_file_path, 'r')
    url = 'webView.loadUrl("' + url + '");}} '
    final_code = get_code_file.read()+url
    android_code_file.write(final_code)
    android_code_file.close()
    
    #remove all the zip files from dir
    for file_path in os.listdir('media/downloads/'):
        os.remove(f'media/downloads/{file_path}')
    
    #create a zip file
    shutil.make_archive(f'media/downloads/{app_name}', 'zip', zip_folder_path)

def account_created_html_email(user):
    subject = 'welcome to Web2App world'
    context = {
        'name' : user.username
    }
    html_message = render_to_string('account-created-email.html',context=context)
    message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    
    try:
        send_mail( subject, message, email_from, recipient_list ,html_message=html_message)
    except:
        pass

def send_liked_html_email(user,liked_app_obj):
    subject = 'Somebody likes your post'
    context = {
        'username' : user.username,
        'liked_user' : liked_app_obj.user,
        'app' : liked_app_obj.app,
    }
    html_message = render_to_string('liked-email.html',context=context)
    message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    try:
        send_mail( subject, message, email_from, recipient_list ,html_message=html_message)
    except:
        pass

def send_commented_html_email(user,commented_app_obj):
    subject = 'Somebody commented on your post'
    context = {
        'username' : user.username,
        'commented_user' : commented_app_obj.user,
        'app' : commented_app_obj.app,
    }
    html_message = render_to_string('comment-email.html',context=context)
    message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    try:
        send_mail( subject, message, email_from, recipient_list ,html_message=html_message)
    except:
        pass


def home(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['name-field'].lower()
        password = request.POST['password-field']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect("login")
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['name-field'].lower()
        email = request.POST['email-field']
        password1 = request.POST['password-field']
        password2 = request.POST['password2-field']
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, "username Already Exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username, email, password1)
                user.save()
                messages.info(request, "Account created successfully")
                account_created_html_email(user)
                return redirect('login')
        else:
            messages.error(request, "Please Enter same Password")
            return redirect('signup')
    return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
   
@login_required(login_url='login')
def profile(request,id):
    basic_user_object = ''
    total_likes = 0
    user_uploaded_apps = AppDetails.objects.filter(user=User.objects.get(id=id),is_upload = True)
    for app in user_uploaded_apps:
        total_likes += Likes.objects.filter(app=app).count()
    try : 
        basic_user_object = UserBasicInfo.objects.get(user=User.objects.get(id=id))
    except:
        UserBasicInfo(user=request.user,email=request.user.email).save()
        basic_user_object = UserBasicInfo.objects.get(user=User.objects.get(id=id))
    
    return render(request, 'profile.html', {
        'user': User.objects.get(id=id),
        'user_info' : basic_user_object,
        'apps': AppDetails.objects.filter(user=User.objects.get(id=id)).order_by('-created_at'),
        'total_uploads' : AppDetails.objects.filter(user=User.objects.get(id=id),is_upload = True),
        'total_likes' : total_likes,
        'likes' : Likes
    })

@login_required(login_url='login')
def editProfile(request):
    user = UserBasicInfo.objects.get(user=request.user)
    form = UserBasicInfoForm(instance=user)
    if request.method == 'POST':
        form = UserBasicInfoForm(instance=user,data = request.POST,files= request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile',request.user.id)
    return render(request, 'editprofile.html',{
        'form' : form,
        'user_info': user,
    })

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        url = request.POST['url-field']
        app_title = request.POST['title-field']
        if AppDetails.objects.filter(app_name=app_title).exists():
            messages.error(request, "App name Already Exists")
            return redirect('upload')
        AppDetails(user=request.user, app_name=app_title,
                   url=url, app_image=image).save()
        

        all_apps = AppDetails.objects.all()
        created_app = all_apps[len(all_apps)-1]
        return redirect('download', created_app.id)
    return render(request, 'upload.html')

@login_required(login_url='login')
def delete_app(request,id):
    app = AppDetails.objects.get(id=id)
    app.delete()
    return redirect('profile',request.user.id)

@login_required(login_url='login')
def upload_app_to_store(request,id):
    app = AppDetails.objects.get(id=id)
    app.is_upload=True
    app.save()
    return redirect('profile',request.user.id)

def app_store(request):
    most_recent_apps = AppDetails.objects.filter(is_upload = True).order_by('-created_at')
    most_popular_apps = AppDetails.objects.filter(is_upload = True).order_by('-total_downloads')
  
    return render(request, 'appstore.html',{
        'most_recent_apps': most_recent_apps,
        'most_popular_apps' : most_popular_apps
    })

def app_page(request, id):
    app = AppDetails.objects.get(id=id)
    is_user_liked = False
    if request.method == "POST":
        app_comment = request.POST['comment']
        comment = Comments(user = User.objects.get(id=request.user.id), app = app, content = app_comment)
        comment.save()
        send_commented_html_email(request.user, comment)
        
    if request.user.is_authenticated:
        is_user_liked = Likes.objects.filter(user = request.user, app = app).exists()
    return render(request, 'app-page.html',{
        'app' : AppDetails.objects.get(id=id),
        'comments' : Comments.objects.filter(app = app).order_by('-created_at'),
        'most_recent_apps': AppDetails.objects.filter(is_upload = True).order_by('-created_at'),
        'is_user_liked' : is_user_liked,
        'total_likes' : Likes.objects.filter(app=app)
    })
    
def edit_app(request, id):
    app = AppDetails.objects.get(id=id)
    if request.method == "POST":
        about_app = request.POST['about']
        app.about = about_app
        app.save()
        return redirect('apppage', app.id)
    return render(request, 'editapp.html',{
        'app' : AppDetails.objects.get(id=id),
    })

@login_required(login_url='login')
def download(request, id):
    app = AppDetails.objects.get(id=id)
    app.total_downloads += 1
    app.save()
    web2app_converter(app.app_name, app.url)
    return render(request, 'download.html', {
        'app': app,
    })

@login_required(login_url='login')
def delete_comment(request,appid,id):
    comment = Comments.objects.get(id=id)
    comment.delete()
    return redirect('apppage', appid)

@login_required(login_url='login')
def like_app(request,id):
    like_obj = Likes(user=request.user, app=AppDetails.objects.get(id=id))
    like_obj.save()
    send_liked_html_email(request.user, like_obj)
    return redirect('apppage', id)

@login_required(login_url='login')
def unlike_app(request,id):
    Likes.objects.get(user=request.user, app=AppDetails.objects.get(id=id)).delete()
    return redirect('apppage', id)