import pyodbc
import Hashing
import ValidChecker
import getapi_2


class database(): 
    def __init__(self, server = 'NIKA', database = 'crypto_db'):
        self.connection_str = f"""
            driver={{ODBC driver 18 for SQL Server}};
            server={server};
            database={database};
            TrustServerCertificate=Yes;
            Trusted_Connection=yes;;
            """.strip()
            
    def get_connection(self):    
        return self.connection_str
    
    def get_data(self, sql_code, sql_input):
        with pyodbc.connect(self.connection_str) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_code, sql_input)
                result = cursor.fetchone()
                return result[0]
            
    def add_data(self, sql_code, sql_input):
        with pyodbc.connect(self.connection_str) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_code, sql_input)
                return True


class sign_up():
    def __init__(self):
        self.db = database()
        
        
    def get_user_info(self):
        self.fname = input("wirte your first name: ")    
        self.lname = input("wirte your last name: ")     
        self.email = input("wirte your email address: ")    
        self.password = input("wirte password: ")
    
    def check(self):
        try: 
            if ValidChecker.check_mail(self.email) == True and  ValidChecker.check_password(self.password) == True:
                return True
        except ValueError as problem:
            print(problem)
        
    def add_user(self):        
        hashing = Hashing.Hashing_password(self.password)
        self.hashed_password = hashing.hashing_scrypt()
        try:
            if_add = self.db.add_data("insert into user_info(fname, lname, email, password_) values(?,?,?,?)", (self.fname, self.lname, self.email, self.hashed_password))
            return if_add
        except pyodbc.IntegrityError:
            print("account with this email is already exist")
            
            
class sign_in():
    def __init__(self):
        self.db = database()
        self.connection_str = self.db.connection_str
        
    def get_user_info(self):
        self.email = input("enter user email: ")
        self.password = input("enter user password: ")
  
    def check(self):
        checkpassword  = Hashing.check_password(self.connection_str ,self.email, self.password)
        if checkpassword.check_hash_password() == True:
            return self.db.get_data("SELECT userid FROM user_info WHERE email = ?", (self.email,))
        else:
            raise ValueError
        
  
class Balance_Operations():
    def __init__(self, user_id):
        self.db = database()
        self.user_id = user_id
        
    def insert_balance(self):
        try:
            if self.db.get_data("select balance from user_info where userid = ?", (self.user_id,)) is None:
                raise ValueError("User not found or balance is not set.")
            balance = float(input("enter your balance: "))
            if balance <= 0:
                raise ValueError("Balance must be a positive number.")
            self.db.add_data("update user_info set balance = ? where userid = ?", (balance, self.user_id))
            print("Balance added successfully.")
        except ValueError as error:
            print(error)
    
    def withdraw_balance(self):
        try:
            balance = float(self.db.get_data("select balance from user_info where userid = ?", (self.user_id,)))
            withdraw_amount = float(input("how much money you want to withdraw: "))
            if withdraw_amount <= 0:
                raise ValueError("Withdraw amount must be a positive number.")
            if withdraw_amount > balance:
                raise ValueError("Insufficient balance.")
            new_balance = balance - withdraw_amount
            self.db.add_data("update user_info set balance = ? where userid = ?", (new_balance, self.user_id))
            print(f"Withdrawal successful. New balance: {new_balance}")
        except ValueError as error:
            print(error)
            
class operations_history():   #დასასრულებელი!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def __init__(self, user_id):
        self.db = database()
        self.user_id = user_id
        
    def add_operation(self, operation_type, amount, crypto_currency = None, price = None, timestramp=None):
        try:
            self.db.add_data("insert into crypto_operations(user_id, crypto_id, operation_type, amount, price_per_unit, total_value, timestamp) values(?,?,?,?,?,?,?)", 
                             (self.user_id, operation_type, crypto_currency, amount, price))
            print("Operation added successfully.")
        except Exception as e:
            print(f"Error adding operation: {e}")
    
    def show_history(self):
        try:
            history = self.db.get_data("select * from operations_history where userid = ?", (self.user_id,))
            return history
        except Exception as e:
            print(f"Error retrieving history: {e}")
                  

class crypto_operations():
    def __init__(self, user_id, crypto_currency):
        self.db = database()
        self.connection_str = self.db.connection_str
        self.user_id = user_id
        self.crypto_currency = crypto_currency
        self.getapi = getapi_2.API_requests(self.crypto_currency)
        
    def insert_balance(self):
        try:
            balance = float(input("enter your balance: "))
            if balance <= 0:
                raise ValueError("Balance must be a positive number.")
            self.db.add_data("update user_info set balance = ? where userid = ?", (self.user_id, balance))
            print("Balance added successfully.")
        except ValueError as error:
            print(error)
    
    def show_price(self):
        self.price = self.getapi.priceAPIcall()
        return self.price 
        
    def buy_crypto(self):
        print("Available cryptocurrencies:", ', '.join(self.crypto_currency))
        coin = input("Which cryptocurrency do you want to buy? ").lower()
        amount = float(input(f"Enter the amount you want to spend: "))
        balance = self.db.get_data("select balance from user_info where userid = ?", (self.user_id,))
        
        if amount > balance:
            raise ValueError("Insufficient balance.")
        
        quantity = self.getapi.purchaseCrypto(coin, amount)
        
        self.db.add_data("insert into crypto_name(name) values(?)",(coin,))
        coin_id = self.db.get_data("select crypto_id from crypto_name where name = ?", (coin,))
        self.db.add_data("insert into user_crypto(userid, crypto_id) values(?,?)", (self.user_id, coin_id))
            
    def sell_crypto(self):
        ...
  
    def convert(self):
        ...
    
    
def main():
    signup = sign_up()
    signin  = sign_in()
    
    print("welcome to our crypto market!")
    answer = input(" 1. sign in \n 2. sign up \n ")
    
    if answer == '1':   
        while True:
            try:
                signin.get_user_info()
            except ValueError as error:
                print(error)
            else:
                user_id = signin.check()
                print("you successfully signed in")
                break
            
        balance_operations = Balance_Operations(user_id)
        action = input(" 1.add balance \n 2.withdraw balance \n 3.skip \n")
        if action == "1":
            balance_operations.insert_balance()
        elif action == "2":
            balance_operations.withdraw_balance()
        elif action == "3":
            pass
        
        while True:
            crypto = input("what cryptocurrency are you interested in? ")
            crypto_list = [coin.strip().lower() for coin in crypto.split(",")]
            crypto_operation = crypto_operations(user_id, crypto_list)
            action = input(" 1.show price \n 2.buy \n 3.sell \n 4.convert \n 5.exit \n")
            
            if action == "1":
                print(crypto_operation.show_price())
                continue
            elif action == "2":
                crypto_operation.buy_crypto()
                continue
            elif action == "3":
                crypto_operation.sell_crypto()
                continue
            elif action == "4":
                crypto_operation.convert()
                continue
            elif action == "5":
                break
            
    elif answer == '2':
         while True:
             signup.get_user_info()
             if signup.check() !=  True:
                 continue
             if signup.add_user() == True: 
                 print("you successfully signed up")
                 break
        
     
if __name__ == "__main__":
    main()