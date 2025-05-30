import requests
import time

latest_prices = {}

def priceAPIcall(crypto_list, vs_currency):
    global latest_prices
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(crypto_list),
        'vs_currencies': vs_currency
    }
    headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz' }

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        latest_prices = response.json()
        for coin in crypto_list:
            coin_id = coin.lower()
            if coin_id in latest_prices:
                price = latest_prices[coin_id][vs_currency.lower()]
                print(f'The price of {coin.title()} in {vs_currency.upper()} is ${price}')
            else:
                print(f'{coin.title()} not found in API response.')
    else:
        print('Failed to retrieve data from the API:', response.status_code)

def purchaseCrypto(vs_currency):
    crypto_name = input("Enter the name of the cryptocurrency you want to purchase: ").strip().lower()
    
    if crypto_name in latest_prices:
        try:
            amount = float(input(f"Enter the amount in {vs_currency.upper()} you want to spend: "))
            price = latest_prices[crypto_name][vs_currency.lower()]
            quantity = amount / price
            print(f"You can purchase {quantity:.6f} {crypto_name.title()} for ${amount}")
        except ValueError:
            print("Invalid amount. Please enter a number.")
    else:
        print("Cryptocurrency not found in the latest price listing. Try after the next update.")

crypto_input = input("Enter the crypto currencies you want to check (comma-separated): ")
vs_currency = input("Enter the currency you want to check in: ")

crypto_list = [coin.strip().lower() for coin in crypto_input.split(",")]

def convertCrypto(crypto_list, vs_currency):
    first_cryptoValue = input("Enter first which you want to exchange: ")
    second_cryptoValue = input("Enter second which you want to exchange it to: ")
    
    if first_cryptoValue in crypto_list and second_cryptoValue in crypto_list:
        try:
            crypto_amount = int(input("Enter how much you want to exchange: "))
            first_price = latest_prices[first_cryptoValue][vs_currency.lower()]
            second_price = latest_prices[second_cryptoValue][vs_currency.lower()]
            converted_amount = (crypto_amount * first_price) / second_price
            print(f"{crypto_amount} of {first_cryptoValue} has been exchanged to {converted_amount} {second_cryptoValue} in {vs_currency}")
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
while True:
    priceAPIcall(crypto_list, vs_currency)
    action = input("\nDo you want to [p]urchase crypto or [w]ait for next update or [e]xchange currencies? (p/w) (q to quit): ").strip().lower()
    if action == 'p':
        purchaseCrypto(vs_currency)
    elif action == 'w':
        print("Waiting 10 seconds for next update...\n")
        time.sleep(10)
    elif action == 'q':
        break
    elif action == 'e':
        convertCrypto(crypto_list, vs_currency)
    else:
        print("Invalid action. Please enter 'p' to purchase crypto or 'w' to wait for next update.")
        action = input("\nDo you want to [p]urchase crypto or [w]ait for next update? (p/w/e) (q to quit): ").strip().lower()
