from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import update_crypto_price
from .models import Wallet
from decimal import Decimal

@login_required(login_url='/login/')
def wallet(request):
    update_crypto_price()
    user_cryptos = Wallet.objects.filter(user=request.user)
    return render(request, 'wallet/wallet.html',{
        'user_cryptos': user_cryptos
    })
    

def insert_money(request):
    if request.method == 'POST':
        deposit_amount = float(request.POST.get('deposit_amount', 0))
        if not deposit_amount <=0:
            user = request.user
            user.balance += Decimal(deposit_amount)
            user.save()
        return redirect('wallet:wallet')
    
    
def withdraw_money(request):
    if request.method == 'POST':
        withdraw_amount = float(request.POST.get('withdraw_amount', 0))
        if not withdraw_amount <= 0:
            user = request.user
            user.balance -= Decimal(withdraw_amount)
            user.save()
        return redirect('wallet:wallet')
        