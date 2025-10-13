from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def sign_up(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        username = fname +" "+ lname
        
        user = User.objects.create_user(
            username = username, 
            email = email, 
            password = password
            )
        user.save()
        
        return redirect('users:login')
    
    return render(request, "users/sign_up.html")


def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
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
