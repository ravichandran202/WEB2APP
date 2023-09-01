from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')


def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def profile(request):
    return render(request,'profile.html')

def upload(request):
    return render(request,'upload.html')

def download(request):
    return render(request,'download.html')
