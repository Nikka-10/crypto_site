from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

@login_required(login_url='/sign_up/login/')
def wallet(request):
    return render(request, 'main/wallet.html')

