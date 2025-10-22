import requests
from .models import Crypto
from django.shortcuts import render, redirect
import time


#decorator
def if_POST(render_page):
    def wrapper(func):
        def inner(request, *args, **kwargs):
            if request.method == "POST":
                return func(request, *args, **kwargs)
            else:
                return render(request, render_page)
        return inner
    return wrapper



def get_crypto_price(crypto_name, max_retries = 3):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    
    headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
                }
    params = {
        'ids': crypto_name,
        'vs_currencies': 'usd'
        }  
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 429:
                print("Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                continue
            else:
                price = response.json()
                price_usd = float(price[crypto_name]['usd'])
                
                return price_usd
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {crypto_name} (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(5)

    
def update_crypto_price():   
    for crypto in Crypto.objects.all():
        crypto_id = crypto.name.lower()
        price = get_crypto_price(crypto_id)
        
        if price:
            crypto.price_usd = price
            crypto.save()
            print(f"Updated {crypto.name}: ${price}")
        else:
            print(f"Skipped {crypto.name} (no price data)")

            
             

        