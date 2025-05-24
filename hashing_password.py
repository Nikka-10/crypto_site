import bcrypt

class Hashing():
    def __init__(self, password):
          self.password = password
    
    def hashing_scrypt(self):
        salt = bcrypt.gensalt()
        b_password = self.password.encode('utf-8')
        hashed_password = bcrypt.hashpw(b_password, salt)
        
        return hashed_password
    
    def check_hash_password(self):
        ...



def main():
    hashing = Hashing()
    

if __name__ == "__main__":
    main()