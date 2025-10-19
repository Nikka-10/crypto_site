from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/sign_up/login/')
def wallet(request):
    return render(request, 'main/wallet.html')