from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import update_crypto_price
from .models import Wallet, Crypto
from decimal import Decimal
from django.views.decorators.http import require_POST
from .models import CustomUser
from .models import History
from django.db import transaction


@login_required(login_url='/login/')
def wallet(request):
    update_crypto_price()
    user_cryptos = Wallet.objects.filter(user=request.user)
    all_crypto = Crypto.objects.all()
    history = History.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wallet/wallet.html',{
        'user_cryptos': user_cryptos,
        'all_crypto': all_crypto,
        'history': history
    })


def add_history(user, operation, amount, crypto=None, converted_crypto=None, getter=None):
    History.objects.create(user=user, operation = operation, crypto=crypto, converted_crypto=converted_crypto, amount = amount, getter=getter)
 

@require_POST
def insert_money(request):
    deposit_amount = float(request.POST.get('deposit_amount', 0))
    if not deposit_amount <=0:
        user = request.user
        user.balance += Decimal(deposit_amount)
        user.save()
        add_history(user=user, operation = "insert", amount = Decimal(deposit_amount))
        return redirect('wallet:wallet')
    
    
@require_POST
def withdraw_money(request):
    withdraw_amount = float(request.POST.get('withdraw_amount', 0))
    user = request.user
    if withdraw_amount > 0 and Decimal(withdraw_amount) <= user.balance:
        user.balance -= Decimal(withdraw_amount)
        user.save()
        add_history(user=user, operation = "withdraw", amount = Decimal(withdraw_amount))
        return redirect('wallet:wallet')
    
    
def buy_crypto(request, name, amount): 
    user = request.user
    crypto = Crypto.objects.get(name=name)
    
    price_unit = crypto.price_usd
    if amount != '':
        total_amount = Decimal(price_unit) * Decimal(amount)
        
        if user.balance >= total_amount:
            user.balance -= total_amount
            user.save()
            
            wallet, created = Wallet.objects.get_or_create(user=user, crypto=crypto)      
            wallet.amount += Decimal(amount)
            add_history(user=user, operation="buy", amount=amount, crypto=crypto)
            wallet.save()    
            
    
    
def sell_crypto(request, name, amount):
    user = request.user
    crypto = Crypto.objects.get(name=name)
    if amount != '':
        money_amount = Decimal(crypto.price_usd) * Decimal(amount)
        
        try:
            wallet = Wallet.objects.get(user=user, crypto=crypto)
        except Wallet.DoesNotExist:
            return
        
        if wallet.amount >= Decimal(amount):
            wallet.amount -= Decimal(amount)
            user.balance += money_amount
            wallet.save()
            user.save()
            add_history(user=user, operation="sell", amount=amount, crypto=crypto)

    
def convert_crypto(request, from_crypto, to_crypto, amount):
    user = request.user
    crypto1 = Crypto.objects.get(name=from_crypto)
    crypto2 = Crypto.objects.get(name=to_crypto)
    
    price1 = crypto1.price_usd
    price2 = crypto2.price_usd
    
    if amount != '':
        total_money = Decimal(price1) * Decimal(amount)
        to_crypto_amount = float(total_money / price2)
        
        
        try:
            wallet1 = Wallet.objects.get(user=user, crypto=crypto1)
            wallet2, created = Wallet.objects.get_or_create(user=user, crypto=crypto2, defaults={'amount': 0})
        except Wallet.DoesNotExist:
            return
        
        if wallet1.amount >= Decimal(amount):
            wallet1.amount -= Decimal(amount)
            wallet2.amount += Decimal(to_crypto_amount)
            wallet1.save()
            wallet2.save()
            add_history(user=user, operation="convert", amount=amount, crypto=crypto1, converted_crypto=crypto2)

        
    
@require_POST
def trade(request):
    operation = request.POST.get('operation')
    
    if operation == 'buy':
        name = request.POST.get('buy-crypto')
        amount = request.POST.get('buy-amount', 0)
        
        buy_crypto(request, name, amount)
        
    elif operation == 'sell':
        name = request.POST.get('sell-crypto')
        amount = request.POST.get('sell-amount', 0)  
        
        sell_crypto(request, name, amount)
        
    elif operation == 'convert':
        from_crypto = request.POST.get('from_crypto')
        to_crypto = request.POST.get('to_crypto')
        amount = request.POST.get('convert-amount', 0)
        
        convert_crypto(request, from_crypto, to_crypto, amount)
    
    return redirect('wallet:wallet')


@require_POST
@transaction.atomic
def transactions(request):
    user = request.user
    getter_email = request.POST.get('email')
    crypto = Crypto.objects.get(name=request.POST.get('crypto_name'))
    
    try:
        getter = CustomUser.objects.get(email=getter_email)
    except CustomUser.DoesNotExist:
        return 'error: Receiver not found'

    crypto = Crypto.objects.get(name=request.POST.get('crypto_name'))

    try:
        user_wallet = Wallet.objects.get(user=user, crypto=crypto)
        getter_wallet, _ = Wallet.objects.get_or_create(user=getter, crypto=crypto)
    except Wallet.DoesNotExist:
        return 'error: You dont own this crypto'
    
    amount = Decimal(request.POST.get('amount'))
    if amount > 0 and user_wallet.amount >= amount:
        user_wallet.amount -= amount
        getter_wallet.amount += amount
        user_wallet.save()
        getter_wallet.save()
        add_history(user=user, operation="send", amount=amount, crypto=crypto, getter=getter)
    return redirect('wallet:wallet')


    
    
    
    
    

    
    
        