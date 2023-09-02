from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path

import shutil
import os

from .models import AppDetails
from .forms import AppDetailsForm
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
    shutil.make_archive(f'media/downloads/{app_name}', 'zip', zip_folder_path)

# Create your views here.


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
                return redirect('login')
        else:
            messages.error(request, "Please Enter same Password")
            return redirect('signup')
    return render(request, 'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def profile(request):
    return render(request, 'profile.html',{
        'user_apps':AppDetails.objects.filter(user=request.user)
    })

def upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        url = request.POST['url-field']
        app_title = request.POST['title-field']
        if AppDetails.objects.filter(app_name=app_title).exists():
            messages.error(request, "App name Already Exists")
            return redirect('upload')
        AppDetails(user=request.user, app_name=app_title, url=url,app_image = image).save()
        web2app_converter(app_title, url)
        
        all_apps = AppDetails.objects.all()
        created_app = all_apps[len(all_apps)-1]
        return redirect('download',created_app.id)
    return render(request, 'upload.html')

# def upload(request):
#     form = AppDetailsForm()
#     if request.method == 'POST':
#         form = AppDetailsForm(data=request.POST , files=request.FILES)
#         if form.is_valid():
#             form.save()
#     return render(request,'newupload.html',{
#         'form' : form
#     })


def download(request,id):
    app = AppDetails.objects.get(id=id)
    return render(request, 'download.html', {
        'app': app,
    })
