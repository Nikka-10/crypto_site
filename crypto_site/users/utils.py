from random import randint
import smtplib


def onetime_code():
    code = ""
    for _ in range(4):
        num = randint(0, 9)
        code += num
    
    return int(code)


def send_email(Receiver):
    
    sender = ""
    receiver = Receiver
    password = ""
    subject = "Khurmax, One-time code"
    body = f"Here is your one-time code:\n {onetime_code()}"

    messege = f"""From: {sender}
    To: {receiver}
    Subject: {subject}\n
    {body} 
    """

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, messege)
    

   