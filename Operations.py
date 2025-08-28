import database
import getapi_2


class crypto_operations():
    def __init__(self, user_id, crypto_currency):
        self.db = database.database()
        self.connection_str = self.db.get_connection()
        self.user_id = user_id
        self.crypto_currency = crypto_currency
        self.getapi = getapi_2.API_requests(self.crypto_currency)
        self.price = None
    
    
    def show_price(self):
        self.price = self.getapi.priceAPIcall()
        return self.price 
        
        
    def buy_crypto(self, coin, amount):
        balance = float(self.db.get_data("select balance from user_info where user_id = ?", (self.user_id,)))
        if amount > balance:
            raise ValueError("Insufficient balance.")
        
        quantity = float(amount) / float(self.getapi.priceAPIcall())
        
        try:
            self.db.add_data("insert into user_crypto(user_id, coin, amount) values(?,?,?)",(self.user_id, coin, quantity))
        except:
            self.db.add_data("update user_crypto set amount = amount + ? where user_id = ? and coin = ?",(quantity, self.user_id, coin))
        finally:
            self.db.add_data("update user_info set balance = ? where user_id = ?", (balance - amount, self.user_id))
        
             
    def sell_crypto(self, coin, amount):
        balance = float(self.db.get_data("select balance from user_info where user_id = ?", (self.user_id,)))
        
        coin_amount_on_balance = float(self.db.get_data("select amount from user_crypto where user_id = ? and coin=?", (self.user_id, coin)))
        
        if not coin_amount_on_balance:
            raise ValueError
        if amount > coin_amount_on_balance:
            raise ValueError
        
        self.db.add_data("update user_crypto set amount = ? where user_id = ? and coin = ?", (coin_amount_on_balance - amount, self.user_id, coin))
        get_money = float(self.getapi.priceAPIcall()) * amount
        self.db.add_data("update user_info set balance = ? where user_id = ?", (balance + get_money, self.user_id))
        
        
    def convert(self):
        ...
    
    