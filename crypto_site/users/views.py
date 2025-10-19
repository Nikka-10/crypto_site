from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate


def sign_up(request):
    if request.method == 'POST':
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
    
    return render(request, "users/sign_up.html")


def log_in(request):
    if request.method == 'POST':
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
               
    return render(request, "users/login.html")

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect("main:index")
