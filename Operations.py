import database
import getapi_2

class crypto_operations():
    def __init__(self, user_id, crypto_currency):
        self.db = database.database()
        self.connection_str = self.db.get_connection()
        self.user_id = user_id
        self.crypto_currency = crypto_currency
        self.getapi = getapi_2.API_requests(self.crypto_currency)
    
    def show_price(self):
        self.price = self.getapi.priceAPIcall()
        return self.price 
        
    def buy_crypto(self):
        print("Available cryptocurrencies:", ', '.join(self.crypto_currency))
        coin = input("Which cryptocurrency do you want to buy? ").lower()
        amount = float(input(f"Enter the amount you want to spend: "))
        balance = float(self.db.get_data("select balance from user_info where userid = ?", (self.user_id,)))
        
        if amount > balance:
            raise ValueError("Insufficient balance.")
        
        quantity = self.getapi.purchaseCrypto(coin, amount)
        
        self.db.add_data("insert into crypto_name(name) values(?)",(coin,))
        coin_id = self.db.get_data("select crypto_id from crypto_name where name = ?", (coin,))
        self.db.add_data("insert into user_crypto(userid, crypto_id) values(?,?)", (self.user_id, coin_id))
        new_balance = self.db.add_data("update user_info set balance = ? where userid = ?", (balance - amount, self.user_id))
        
        
            
    def sell_crypto(self):
        ...
  
    def convert(self):
        ...
    
    