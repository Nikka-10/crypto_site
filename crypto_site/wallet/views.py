from django.shortcuts import render, redirect
from .utils import if_POST
from django.contrib.auth.decorators import login_required
from .utils import update_crypto_price
from .models import Wallet, Crypto
from decimal import Decimal
from django.views.decorators.http import require_POST


@login_required(login_url='/login/')
def wallet(request):
    update_crypto_price()
    user_cryptos = Wallet.objects.filter(user=request.user)
    all_crypto = Crypto.objects.all()
    return render(request, 'wallet/wallet.html',{
        'user_cryptos': user_cryptos,
        'all_crypto': all_crypto
    })
 
 
@require_POST
def insert_money(request):
    deposit_amount = float(request.POST.get('deposit_amount', 0))
    if not deposit_amount <=0:
        user = request.user
        user.balance += Decimal(deposit_amount)
        user.save()
        return redirect('wallet:wallet')
    
    
@require_POST
def withdraw_money(request):
    withdraw_amount = float(request.POST.get('withdraw_amount', 0))
    user = request.user
    if withdraw_amount > 0 and Decimal(withdraw_amount) <= user.balance:
        user.balance -= Decimal(withdraw_amount)
        user.save()
        return redirect('wallet:wallet')
    
    
def buy_crypto(request, name, amount):
    ...
  
    
def sell_crypto(request, name, amount):
    ...
  
    
def convert_crypto(request, from_crypto, to_crypto, amount):
    ...
  
    
@require_POST
def trade(request):
    operation = request.POST.get('operation')
    
    if operation == 'buy':
        name = request.POST.get('crypto')
        amount = float(request.POST.get('amount', 0))
        
        buy_crypto(request, name, amount)
    elif operation == 'sell':
        name = request.POST.get('crypto')
        amount = float(request.POST.get('amount', 0))    
            
        sell_crypto(request, name, amount)
    elif operation == 'convert':
        from_crypto = request.POST.get('from_crypto')
        to_crypto = request.POST.get('to_crypto')
        amount = float(request.POST.get('amount', 0))
        
        convert_crypto(request, from_crypto, to_crypto, amount)
    
    
        