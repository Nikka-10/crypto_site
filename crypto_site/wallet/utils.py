import requests
from .models import Crypto
import time

def update_crypto_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    
    headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
                }
    
    for crypto in Crypto.objects.all():
        params = {
            'ids': crypto.name.lower(),
            'vs_currencies': 'usd'
            }
        try:    
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 429:
                print("Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                continue
                
            
            price = response.json()
            crypto.price_usd = float(price[crypto.name]['usd'])
            crypto.save()
            
        except requests.exceptions.RequestException as e:
             print(f"Error updating {crypto.name}: {e}")
             

        