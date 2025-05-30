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


class sign_up():
    def __init__(self, connection_str):
        self.connection_str = connection_str

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
            with pyodbc.connect(self.connection_str) as conn:
                cursor = conn.cursor()
                cursor.execute(f"insert into user_info(fname, lname, email, password_) values(?,?,?,?)", (self.fname, self.lname, self.email, self.hashed_password))
                
                return True
        except pyodbc.IntegrityError:
            print("account with this email is already exist")
            
            
class sign_in():
    def __init__(self, connection_str):
        self.connection_str = connection_str
        
    def get_user_info(self):
        self.email = input("enter user email: ")
        self.password = input("enter user password: ")
  
    def check(self):
        checkpassword  = Hashing.check_password(self.connection_str ,self.email, self.password)
        if checkpassword.check_hash_password() == True:
            return True
        
  
class crypto_operations():
    def __init__(self, crypto_currency):
        self.crypto_currency = crypto_currency
        self.getapi = getapi_2.API_requests(self.crypto_currency)
    
    def show_price(self):
        self.price = self.getapi.priceAPIcall()
        return self.price 
        
    def buy_crypto(self):
        ...
        
    def sell_crypto(self):
        ...
  
    def convert(self):
        ...
    
    
def main():
    db = database()
    connection_str = db.get_connection()
    signup = sign_up(connection_str)
    signin  = sign_in(connection_str)
    
    print("welcome to our crypto market!")
    answer = input(" 1. sign in \n 2. sign up \n ")
    
    if answer == '1':
        while True:
            signin.get_user_info()
            
            if signin.check() == True:
                print("you successfully signed in")
                break
            else:
                print("login or password is incorrect")
                
    elif answer == '2':
        
        crypto = input("what cryptocurrency are you interested in? ")
        crypto_list = [coin.strip().lower() for coin in crypto.split(",")]
        action = input(" 1.show price \n 2.buy \n 3.sell \n 4.convert \n")
        crypto_operation = crypto_operations(crypto_list)
        if action == 1:
            print(crypto_operation.show_price())
        elif action == 2:
            pass
        elif action == 3:
            pass
        elif action == 4:
            pass
        
       # while True:
       #     signup.get_user_info()
       #     if signup.check() !=  True:
       #         continue
       #     if signup.add_user() == True: 
       #         print("you successfully signed up")
       #         break
            
            
       
  
     
if __name__ == "__main__":
    main()