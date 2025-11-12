from django.shortcuts import redirect
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from wallet.utils import if_POST
from .utils import onetime_code
from .utils import send_email


@if_POST("users/sign_up.html")
def sign_up(request):
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    username = first_name +" "+ last_name
    
    one_time_code = onetime_code()
    send_email(email, one_time_code)
    
    request.session['signup_data'] = {
    'username': username,
    'email': email,
    'password': password,
    'first_name': first_name,
    'last_name': last_name, 
    'code': one_time_code
        }
    
    return redirect('users:verify_2fa')

        
@if_POST("users/login.html")
def log_in(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
        user_obj = CustomUser.objects.get(email=email)
        user = authenticate(request, username=user_obj.username, password=password)
    except CustomUser.DoesNotExist:
        user = None
    
    if  not user:
        return redirect("users:sign_up")
    
    if user_obj.has_2FA:
        one_time_code = onetime_code()
        send_email(email, one_time_code)
        request.session['user_id'] = user_obj.id
        request.session['one_time_code'] = one_time_code
        return redirect("users:verify_2fa")
    else:
        login(request, user)
        return redirect('main:index')
            

def log_out(request):
    logout(request)
    return redirect('main:index')


def toggle_2fa(request):
    user = request.user
    
    if user.has_2fa:
        user.has_2fa = False
    else:
        user.has_2fa = True
        
    user.save()
        
        
@if_POST('users/confirm_mail.html')
def verify_2fa(request):
    entered_code = "".join([request.POST[f'd{i}'] for i in range(1, 5)])

    user_id = request.session.get('user_id')
    one_time_code = request.session.get('one_time_code')
    signup_data = request.session.get('signup_data')

    if user_id and entered_code == one_time_code:
        user = CustomUser.objects.get(id=user_id)
        login(request, user)

        del request.session['user_id']
        del request.session['one_time_code']

        return redirect("wallet:wallet")

    elif signup_data and entered_code == signup_data['code']:
        CustomUser.objects.create_user(
            username=signup_data['username'],
            email=signup_data['email'],
            password=signup_data['password']
        )

        del request.session['signup_data']
        return redirect("users:login")

    return redirect("users:login")