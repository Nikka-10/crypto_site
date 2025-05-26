import bcrypt
import pyodbc

class Hashing_password():
    def __init__(self, password):
        self.password = password
    
    def hashing_scrypt(self):
        salt = bcrypt.gensalt()
        b_password = self.password.encode('utf-8')
        hashed_password = bcrypt.hashpw(b_password, salt)
        
        return hashed_password


class check_password():
    def __init__(self, connection_str, email, entered_password):
        self.connection_str = connection_str
        self.email = email
        self.entered_password = entered_password.encode("utf-8")
    
    def check_hash_password(self):
        with (pyodbc.connect(self.connection_str)) as conn:
            cursor = conn.cursor()
            cursor.execute("select password_ from user_info where email = ?",(self.email,))
            row = cursor.fetchone()
            
            saved_password = row[0].encode('utf-8')
            print(saved_password)
            
            if bcrypt.checkpw(self.entered_password, saved_password):
                return True
            else:
                return False
            


def main():
    ...
    

if __name__ == "__main__":
    main()