import database
import getapi_2


class crypto_operations():
    def __init__(self, user_id):
        self.db = database.database()
        self.connection_str = self.db.get_connection()
        self.user_id = user_id
        self.price = None
    
    
    def show_price(self, coin: str) -> None:
        api_call = getapi_2.API_requests(coin)
        self.price = api_call.priceAPIcall()
        return self.price 
        
        
    def buy_crypto(self, coin, amount) -> None:
        balance = float(self.db.get_data("select balance from user_info where user_id = ?", (self.user_id,)))
        if amount > balance:
            raise ValueError("Insufficient balance.")
        
        api_call = getapi_2.API_requests(coin)
        quantity = float(amount) / float(api_call.priceAPIcall())
        
        try:
            self.db.add_data("update user_crypto set amount = amount + ? where user_id = ? and coin = ?",(quantity, self.user_id, coin))
        except:
            self.db.add_data("insert into user_crypto(user_id, coin, amount) values(?,?,?)",(self.user_id, coin, quantity))
        finally:
            self.db.add_data("update user_info set balance = ? where user_id = ?", (balance - amount, self.user_id))
        
             
    def sell_crypto(self, coin, amount) -> None:
        balance = float(self.db.get_data("select balance from user_info where user_id = ?", (self.user_id,)))
        
        coin_amount_on_balance = float(self.db.get_data("select amount from user_crypto where user_id = ? and coin=?", (self.user_id, coin)))
        
        if not coin_amount_on_balance:
            raise ValueError
        if amount > coin_amount_on_balance:
            raise ValueError
        
        self.db.add_data("update user_crypto set amount = ? where user_id = ? and coin = ?", (coin_amount_on_balance - amount, self.user_id, coin))
        api_call = getapi_2.API_requests(coin)
        get_money = float(api_call.priceAPIcall()) * amount
        self.db.add_data("update user_info set balance = ? where user_id = ?", (balance + get_money, self.user_id))
        
        
    def convert(self, coin_1: str, amount_1: int, coin_2: str) -> None:
        api_call = getapi_2.API_requests(coin_1)
        price_1 = api_call.priceAPIcall()
        
        api_call = getapi_2.API_requests(coin_2)
        price_2 = api_call.priceAPIcall()
        
        received_coin_amount = (price_1 * amount_1)/price_2
        
        coin_amoun_on_balance = self.db.get_data("select amount from user_crypto where user_id = ? and coin = ?", (self.user_id, coin_1))
        if int(coin_amoun_on_balance) < amount_1:
            raise ValueError
        
        self.db.add_data("update user_crypto set amount = amount - ? where user_id = ? and coin = ?", (amount_1, self.user_id, coin_1))
        try:
            self.db.add_data("update user_crypto set amount = amount + ? where user_id = ? and coin = ?", (received_coin_amount, self.user_id, coin_2))
        except:
            self.db.add_data("insert into user_crypto(user_id, coin, amount) values(?,?,?)",(self.user_id, coin_2, received_coin_amount))
            
        
    def send_crypto(self, recipient_id, coin, amount):
        coin_amoun_on_balance = self.db.get_data("select amount from user_crypto where user_id = ? and coin = ?", (self.user_id, coin))
        if int(coin_amoun_on_balance) < amount:
            raise ValueError
        
        self.db.add_data("update user_crypto set amount = amount - ? where user_id = ? and coin = ?", (amount, self.user_id, coin))
        
        try:
            self.db.add_data("update user_crypto set amount = amount + ? where user_id = ? and coin = ?", (amount, recipient_id, coin))
        except:
            self.db.add_data("insert into user_crypto(user_id, coin, amount) values(?,?,?)",(recipient_id, coin, amount))
          
    