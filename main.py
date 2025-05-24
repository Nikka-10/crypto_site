import pyodbc
import bcrypt
import hashing_password


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

    def get_user_info():
        fname = input("wirte your first name: ")    
        lname = input("wirte your last name: ")    
        email = input("wirte your email address: ")    
        password = input("wirte password: ")
        
        return fname, lname, email, password
        
    def add_user(self, Firstname, Lastname, email, password):
        salt = bcrypt.gensalt()
        b_password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(b_password, salt)
        
        with pyodbc.connect(self.connection_str) as conn:
            cursor = conn.cursor()
            cursor.execute(f"insert into user_info(fname, lname, email, password_) values(?,?,?,?)", (Firstname, Lastname, email, hashed_password))
            
            cursor.close()
            
            
class sign_in():
    def __init__(self, login, password):
        self.login = login
        self.password = password
        
    def check():
        ...

    
class Valid_Checker():
    def __init__(self, mail, password):
        self.mail = mail
        self.password = password
    
    def check_mail(self):
        if '@' not in self.mail:
            return "mail must contain symbol '@'"
        return True
   
    def check_password(self):
        if len(self.password) < 8:
            return "password must contain at least 8 symbols"
        if self.password.isupper():
            return "password must contain lowercase letters"
        if self.password.islower():
            return "password must contain uppercase letters"
        if self.password.isnumeric():
            return "password must contain letters"
        if self.password.isalpha():
            return "password must contain numeric characters"
        
        return True
    
def main():
    print("welcome to our crypto market!")
    answer = input(" 1. sign in \n 2. sign up \n ")
    
    if answer == '1':
        pass
    elif answer == '2':
       fname, lname, email, password =  sign_up.get_user_info()
    
    db = database()
    connection_str = db.get_connection()
    
    signup = sign_up(connection_str)
    adduser = signup.add_user(fname, lname, email, password)
    
     
if __name__ == "__main__":
    main()