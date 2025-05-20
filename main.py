import pyodbc
import requests


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


class User():
    def __init__(self, connection_str):
        self.connection_str = connection_str

    
    def add_user(self, Firstname, Lastname, email, password):
        with pyodbc.connect(self.connection_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"insert into user_info(fname, lname, email, password_) values(?,?,?,?)", (Firstname, Lastname, email, password))
            
            cursor.close()
    

class crypto_operatinos():
    def __init__(self, connection):
        self.connection = connection
         
    def Get_crypto(self,):
        ...
    
    def buy_crypto(self,):
        ...
        
    def sell_crypto(self,):
        ...
        
    def check_wallet(self,):
        ...
        
  
     
def main():
    db = database()
    connection_str = db.get_connection()
    
    user = User(connection_str)
    crupto_op = crypto_operatinos(connection_str)
    
    fname, lname, email, password = get_user_info()
    user.add_user(fname, lname, email, password)
  
    
def get_user_info():
    fname = input("wirte your first name: ")    
    lname = input("wirte your last name: ")    
    email = input("wirte your email address: ")    
    password = input("wirte password: ")
    
    return fname, lname, email, password    
    
    
if __name__ == "__main__":
    main()