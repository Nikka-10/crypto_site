import requests
import time
url = 'https://api.coingecko.com/api/v3/simple/price'
params = {  
         'ids': 'bitcoin,ethereum',
         'vs_currencies': 'USD'
}

headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz' }

response = requests.get(url, params = params)
def priceAPIcall():
    if response.status_code == 200:
        data = response.json()
        Bitcoin_price = data['bitcoin']['usd']
        Ethereum_price = data['ethereum']['usd']
        print(f'The price of Ethereum in USD is ${Ethereum_price}')
        print(f'The price of Bitcoin in USD is ${Bitcoin_price}')
    else:
        print('Failed to retrieve data from the API')

while True:
    priceAPIcall()
    time.sleep(20)
