def main():
    name, Lname, mail, password = "nika", "gvasalia", "somemail@gmail.com", "password"
    if check_mail(mail) == True: 
        print("mail is valid")
    else:
        print(check_mail(mail))
        
    if chech_password(password) == True:
         print("password is valid")
    else:
        print(chech_password(password))
    
   
  
def check_mail(mail):
    if '@' in mail:
        return "mail must contain symbol '@'"
    return True
   
    
def chech_password(password):
    if len(password) < 8:
        return "password must contain at least 8 symbols"
    if password.isalnum():
        return "password must contain letters"
    if password.isalpha():
        return "password must contain numeric characters"
    
    return True
    
    
      
if __name__ == "__main__":
    main()