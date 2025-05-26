import pyodbc
import bcrypt
import Hashing
import ValidChecker


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
                print("you successfully signed up")
        except ValueError:
            print(ValueError)
        
    def add_user(self):        
        hashing = Hashing.Hashing_password(self.password)
        self.hashed_password = hashing.hashing_scrypt()
        
        with pyodbc.connect(self.connection_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"insert into user_info(fname, lname, email, password_) values(?,?,?,?)", (self.fname, self.lname, self.email, self.hashed_password))
            
            cursor.close()
            
            
class sign_in():
    def __init__(self, connection_str):
        self.connection_str = connection_str
        
    def get_user_info(self):
        self.email = input("enter user email: ")
        self.password = input("enter user password: ")
  
    def check(self):
        checkpassword  = Hashing.check_password(self.connection_str ,self.email, self.password)
        if checkpassword.check_hash_password() == True:
            print("you successfully signed in")
        else:
            print("login or password is incorrect")
        
  
class crypto_operations():
    ...
  
    
def main():
    db = database()
    connection_str = db.get_connection()
    signup = sign_up(connection_str)
    signin  = sign_in(connection_str)
    
    print("welcome to our crypto market!")
    answer = input(" 1. sign in \n 2. sign up \n ")
    
    if answer == '1':
        signin.get_user_info()
        signin.check()
        
    elif answer == '2':
       signup.get_user_info()
       signup.check()
       signup.add_user()
       
  
     
if __name__ == "__main__":
    main()