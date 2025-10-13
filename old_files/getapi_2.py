import requests
import json


class API_requests():
    
    def __init__(self, crypto_currency: str, vs_currency: str = 'usd'):
        self.crypto_currency = crypto_currency
        self.vs_currency = vs_currency
        
        url = 'https://api.coingecko.com/api/v3/simple/price'
        
        params = {
            'ids': f'{crypto_currency}',
            'vs_currencies': vs_currency
        }
        headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0'
                   }
        
        self.response = requests.get(url, params=params, headers=headers)
    
    
    def priceAPIcall(self) -> int:
        price = self.response.json()
        return int(price[self.crypto_currency][self.vs_currency])
        
