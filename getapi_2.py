import requests
import time


class API_requests():
    def __init__(self, crypto_list, vs_currency = 'usd'):
        self.crypto_list = crypto_list
        self.vs_currency = vs_currency
        
        url = 'https://api.coingecko.com/api/v3/simple/price'
        params = {
            'ids': ','.join(crypto_list),
            'vs_currencies': vs_currency
        }
        headers = { 'x-cg-demo-api-key': 'CG-Um1wPk1y9NhixNZxRh5jb2vz' }
        
        self.response = requests.get(url, params=params, headers=headers)
    
    def priceAPIcall(self):
        if self.response.status_code != 200:
            return 'Failed to retrieve data from the API:', self.response.status_code
        
        self.latest_prices = self.response.json()
        for coin in self.crypto_list:
            if coin.lower() in self.latest_prices:
                price = self.latest_prices[coin.lower()][self.vs_currency.lower()]
                return f'The price of {coin.title()} in {self.vs_currency.upper()} is ${price}'
            else:
                return f'{coin.title()} not found in API response.'

    def purchaseCrypto(self):
        crypto_name = input("Enter the name of the cryptocurrency you want to purchase: ").strip().lower()

        if crypto_name not in self.latest_prices:
            print("Cryptocurrency not found in the latest price listing. Try after the next update.")
            return
        try:
            amount = float(input(f"Enter the amount in {self.vs_currency.upper()} you want to spend: "))
            price = self.latest_prices[crypto_name][self.vs_currency.lower()]
            quantity = amount / price
            print(f"You can purchase {quantity:.6f} {crypto_name.title()} for ${amount}")
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def convertCrypto(self):
        first_cryptoValue = input("Enter first which you want to exchange: ")
        second_cryptoValue = input("Enter second which you want to exchange it to: ")
        
        if first_cryptoValue in self.crypto_list and second_cryptoValue in self.crypto_list:
            try:
                crypto_amount = int(input("Enter how much you want to exchange: "))
                first_price = self.latest_prices[first_cryptoValue][self.vs_currency.lower()]
                second_price = self.latest_prices[second_cryptoValue][self.vs_currency.lower()]
                converted_amount = (crypto_amount * first_price) / second_price
                print(f"{crypto_amount} of {first_cryptoValue} has been exchanged to {converted_amount} {second_cryptoValue} in {self.vs_currency}")
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        
    
    
    
def main():
    ...

    
if __name__ == "__main__":
    main()