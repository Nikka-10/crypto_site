from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from wallet.utils import if_POST


@if_POST("users/sign_up.html")
def sign_up(request):
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    username = first_name +" "+ last_name
    
    user = CustomUser.objects.create_user(
        username = username, 
        email = email, 
        password = password,
        first_name=first_name,
        last_name=last_name 
        )
    user.save()
    return redirect('users:login')

        
@if_POST("users/login.html")
def log_in(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user_obj = CustomUser.objects.get(email=email)
        user = authenticate(request, username=user_obj.username, password=password)
    except CustomUser.DoesNotExist:
        user = None
    
    if user:
        login(request, user)
        return redirect('main:index')
    else:
        return redirect("users/sign_up.html")
            

def log_out(request):
    logout(request)
    return redirect('main:index')
