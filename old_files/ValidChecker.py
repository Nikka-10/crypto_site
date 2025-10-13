def check_mail(mail):
    if '@' not in mail:
        raise ValueError("mail must contain symbol '@'")
    return True

def check_password(password):
    if len(password) < 8:
        raise ValueError("password must contain at least 8 symbols")
    if password.isupper():
        raise ValueError("password must contain lowercase letters")
    if password.islower():
        raise ValueError("password must contain uppercase letters")
    if password.isnumeric():
        raise ValueError("password must contain letters")
    if password.isalpha():
        raise ValueError("password must contain numeric charactraise")
    return True
    