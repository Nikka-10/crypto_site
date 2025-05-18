import pyodbc
import requests


class user():
    def __init__(self, Firstname, Lastname, email, password):
        pass
        

class crypto_operatinos():
    def __init__(self, connection):
        self.connection = connection
         
    def Get_crypto(self,):#ვფიქრობ კრიპტოს საიტიდან აღების ფუნქციას რომ გავაკეთებთ აქ ჩასმა შეიძლება და სახელი, ფასის, ცვლილებების და სხვა ინფოს შენახვა
        ...
    
    def buy_crypto(self,):
        ...
        
    def sell_crypto(self,):
        ...
        
    def check_wallet(self,):
        ...
        
  
    
class database():
    
    def __init__(self, server = 'NIKA', database = 'crypto_base'): # საბოლოოდ რაიმე ღია მონაცემთა ბაზაზე შეიცვლება
        self.connection_string = f"""
            driver={{ODBC driver 18 for SQL Server}};
            server={server};
            database={database};
            TrustServerCertificate=yes;
            Trusted_Connection=yes
            """
        self.connection = pyodbc.connect(self.connection_string)
            

    
def main():
    db = database()
    crupto_op = crypto_operatinos(db.connection)
    
    
if __name__ == "__main__":
    main()