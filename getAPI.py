import requests
import time

def priceAPIcall(crypto_list, vs_currency):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(crypto_list),
        'vs_currencies': vs_currency
    }
    headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz' }

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        for coin in crypto_list:
            coin_id = coin.lower()
            if coin_id in data:
                price = data[coin_id][vs_currency.lower()]
                print(f'The price of {coin.title()} in {vs_currency.upper()} is ${price}')
            else:
                print(f'{coin.title()} not found in API response.')
    else:
        print('Failed to retrieve data from the API:', response.status_code)

crypto_input = input("Enter the crypto currencies you want to check (comma-separated): ")
vs_currency = input("Enter the currency you want to check in: ")

crypto_list = [coin.strip().lower() for coin in crypto_input.split(",")]

while True:
    priceAPIcall(crypto_list, vs_currency)
    time.sleep(20)
