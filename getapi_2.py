import requests

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
        if self.response.status_code == 200:
            self.latest_prices = self.response.json()
        else:
            self.latest_prices = {}
    
    def priceAPIcall(self):
        if self.response.status_code != 200:
            return 'Failed to retrieve data from the API:', self.response.status_code
        
        for coin in self.crypto_list:
            if coin.lower() in self.latest_prices:
                price = self.latest_prices[coin.lower()][self.vs_currency.lower()]
                return f'The price of {coin.title()} in {self.vs_currency.upper()} is ${price}'
            else:
                return f'{coin.title()} not found in API response.'

    def purchaseCrypto(self,coin,amount):

        if coin not in self.latest_prices:
            print(f"{coin.title()} not found in the latest price listing.")
            return
        try:
            price = self.latest_prices[coin][self.vs_currency]
            quantity = amount / price
            print(f"You can purchase {quantity:.6f} {coin.title()} for ${amount}")
            return quantity
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