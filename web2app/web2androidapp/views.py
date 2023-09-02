from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request,'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['name-field'].lower()
        password = request.POST['password-field']
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.error(request,'Username or Password is incorrect')
            return redirect("login")
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['name-field'].lower()
        email = request.POST['email-field']
        password1 = request.POST['password-field']
        password2 = request.POST['password2-field']
        if password1==password2:
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email Already Exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request,"username Already Exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username,email,password1)
                user.save()
                messages.info(request,"Account created successfully")
                return redirect('login')
        else:
            messages.error(request,"Please Enter same Password")
            return redirect('signup')
    return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def profile(request):
    return render(request,'profile.html')

def upload(request):
    return render(request,'upload.html')

def download(request):
    return render(request,'download.html')
