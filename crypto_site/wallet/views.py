from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .utils import update_crypto_price
from .models import Wallet, Crypto
from decimal import Decimal, InvalidOperation
from django.views.decorators.http import require_POST
from .models import CustomUser
from .models import History
from django.db import transaction


@login_required(login_url='/login/')
def render_wallet(request,error_type=None, error=None):
    update_crypto_price()
    user_cryptos = Wallet.objects.filter(user=request.user)
    all_crypto = Crypto.objects.all()
    history = History.objects.filter(user=request.user).order_by('-id')
    
    context = {
        'user_cryptos': user_cryptos,
        'all_crypto': all_crypto,
        'history': history,       
    }    
    if error:
        context[error_type] = error  

    return render(request, "wallet/wallet.html", context)

def add_history(user, operation, amount, crypto=None, converted_crypto=None, getter=None):
    History.objects.create(user=user, operation = operation, crypto=crypto, converted_crypto=converted_crypto, amount = amount, getter=getter)
 

@require_POST
def insert_money(request):
    raw_amount = request.POST.get('deposit_amount')
    max_balance = Decimal('999999999999999999.99')
    user = request.user
    
    try:
        deposit_amount = Decimal(raw_amount)
    except (InvalidOperation, TypeError):
        return render_wallet(request, "Invalid amount entered")
    
    if user.balance + deposit_amount > max_balance:
        return render_wallet(request, "insert_error", "let's be honest, you don't have that much money" )
    
    if deposit_amount <=0:
        return render_wallet(request, "insert_error", "Amount must be positive" )
    
    user = request.user
    user.balance += Decimal(deposit_amount)
    user.save()
    add_history(user=user, operation = "insert", amount = Decimal(deposit_amount))
    return redirect('wallet:wallet')
    
    
@require_POST
def withdraw_money(request):
    withdraw_amount = Decimal(request.POST.get('withdraw_amount', 0))
    user = request.user
    
    if not withdraw_amount > 0:
        return render_wallet(request, "withdraw_error", "amount must be positive number" )
        
    if not Decimal(withdraw_amount) <= user.balance:
        return render_wallet(request, "withdraw_error", "not enought balance" )
        
    user.balance -= Decimal(withdraw_amount)
    user.save()
    add_history(user=user, operation = "withdraw", amount = Decimal(withdraw_amount))
    return redirect('wallet:wallet')

    
def buy_crypto(request, name, amount): 
    user = request.user
    crypto = Crypto.objects.get(name=name)
    
    price_unit = crypto.price_usd
    if amount == '':
        return render_wallet(request,"trade_error", "write amount of crypto currency you want to buy")
               
    total_amount = Decimal(price_unit) * Decimal(amount)
    
    if user.balance < total_amount:
        return render_wallet(request,"trade_error", "not enought balance")
                
    user.balance -= total_amount
    user.save()
    
    wallet, created = Wallet.objects.get_or_create(user=user, crypto=crypto)      
    wallet.amount += Decimal(amount)
    add_history(user=user, operation="buy", amount=amount, crypto=crypto)
    wallet.save()
    return redirect('wallet:wallet')
            
      
def sell_crypto(request, name, amount):
    user = request.user
    crypto = Crypto.objects.get(name=name)
    if amount != '':
        money_amount = Decimal(crypto.price_usd) * Decimal(amount)
        
        try:
            wallet = Wallet.objects.get(user=user, crypto=crypto)
        except Wallet.DoesNotExist:
            return render_wallet(request,"trade_error", "we dont have that crypto")          
        
        if wallet.amount >= Decimal(amount):
            wallet.amount -= Decimal(amount)
            user.balance += money_amount
            wallet.save()
            user.save()
            add_history(user=user, operation="sell", amount=amount, crypto=crypto)
            return redirect('wallet:wallet')
            
        return render_wallet(request,"trade_error", "not enought amount of crypto currency")
            
    return render_wallet(request,"trade_error", "write amount of crypto currency you want to sell")

    
def convert_crypto(request, from_crypto, to_crypto, amount):
    user = request.user
    crypto1 = Crypto.objects.get(name=from_crypto)
    crypto2 = Crypto.objects.get(name=to_crypto)
    
    price1 = crypto1.price_usd
    price2 = crypto2.price_usd
    
    if amount != '':
        total_money = Decimal(price1) * Decimal(amount)
        to_crypto_amount = Decimal(total_money / price2)
        
        
        try:
            wallet1 = Wallet.objects.get(user=user, crypto=crypto1)
            wallet2, created = Wallet.objects.get_or_create(user=user, crypto=crypto2, defaults={'amount': 0})
        except Wallet.DoesNotExist:
            return render_wallet(request,"trade_error", "how you even get this error?")
        
        if wallet1.amount >= Decimal(amount):
            wallet1.amount -= Decimal(amount)
            wallet2.amount += Decimal(to_crypto_amount)
            wallet1.save()
            wallet2.save()
            add_history(user=user, operation="convert", amount=amount, crypto=crypto1, converted_crypto=crypto2)
            return redirect('wallet:wallet')
            
        return render_wallet(request,"trade_error", "not enought amount of crypto currency")
            
    return render_wallet(request,"trade_error", "write amount of crypto currency you want to convert")

        
    
@require_POST
def trade(request):
    operation = request.POST.get('operation')
    
    if operation == 'buy':
        name = request.POST.get('buy-crypto')
        amount = request.POST.get('buy-amount', 0)
        
        return buy_crypto(request, name, amount)
        
    elif operation == 'sell':
        name = request.POST.get('sell-crypto')
        amount = request.POST.get('sell-amount', 0)  
        
        return sell_crypto(request, name, amount)
        
    elif operation == 'convert':
        from_crypto = request.POST.get('from_crypto')
        to_crypto = request.POST.get('to_crypto')
        amount = request.POST.get('convert-amount', 0)
        
        return convert_crypto(request, from_crypto, to_crypto, amount)
    else:
        return render_wallet(request,"trade_error", "not valid operation")
    


@require_POST
@transaction.atomic
def transactions(request):
    user = request.user
    getter_email = request.POST.get('email')
    crypto = Crypto.objects.get(name=request.POST.get('crypto_name'))
    
    try:
        getter = CustomUser.objects.get(email=getter_email)
    except CustomUser.DoesNotExist:
        return render_wallet(request, "tarnsaction_error", "Receiver not found")

    crypto = Crypto.objects.get(name=request.POST.get('crypto_name'))

    try:
        user_wallet = Wallet.objects.get(user=user, crypto=crypto)
    except Wallet.DoesNotExist:
        return render_wallet(request, "tarnsaction_error", "you dont own this crypto")
    
    getter_wallet, _ = Wallet.objects.get_or_create(user=getter, crypto=crypto)
    
    if not getter_wallet:
        return render_wallet(request, "tarnsaction_error", "you dont own this crypto")
        
    amount = Decimal(request.POST.get('amount'))
    
    if not amount > 0:
        return render_wallet(request, "tarnsaction_error", "amount must be positive number")
        
    if not user_wallet.amount >= amount:
        return render_wallet(request, "tarnsaction_error", "not enought amount of crypto currency")
        
    user_wallet.amount -= amount
    getter_wallet.amount += amount
    user_wallet.save()
    getter_wallet.save()
    add_history(user=user, operation="send", amount=amount, crypto=crypto, getter=getter)
    add_history(user=getter, operation="get", amount=amount, crypto=crypto, getter=user)
    
    return redirect('wallet:wallet')
    