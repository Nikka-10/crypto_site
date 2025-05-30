import requests
import time
#import PyCurrency_Converter

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
    

#class convert():
#    def __init__(self, crypto_amount, currency):
#        self.crypto_amount = crypto_amount
#        self.currency = currency
#        
#    def convert_price(self):
#        converted_price = PyCurrency_Converter.convert(self.crypto_amount, 'USD', self.currency)
#        return converted_price
#    
#    def convert_crypto(self, new_crypto):
#        ...
        
    
    
    
def main():
    crypto_input = input("Enter the crypto currencies you want to check (comma-separated): ")
    vs_currency = input("Enter the currency you want to check in: ")
    crypto_list = [coin.strip().lower() for coin in crypto_input.split(",")]
    
    api_requests = API_requests(crypto_list, vs_currency)
    
    while True:
        api_requests.priceAPIcall()
        action = input("\nDo you want to [p]urchase crypto or [w]ait for next update? (p/w): ").strip().lower()
        if action == 'p':
            api_requests.purchaseCrypto()
        elif action == 'w':
            print("Waiting 20 seconds for next update...\n")
            time.sleep(20)
        else:
            break


    
if __name__ == "__main__":
    main()