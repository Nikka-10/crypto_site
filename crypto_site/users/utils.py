from random import randint
import smtplib


def onetime_code():
    code = ""
    for _ in range(4):
        num = randint(0, 9)
        code += str(num)
    
    return code


def send_email(Receiver, one_time_code):
    
    sender = "nikoloz.gvasalia@gau.edu.ge" # gonna write later
    receiver = Receiver
    password = "tsst hieg naka amox" # gonna write later
    subject = "Khurmax, One-time code"
    body = f"Here is your one-time code:\n {one_time_code}"

    messege = f"""From: {sender}
    To: {receiver}
    Subject: {subject}\n
    {body} 
    """
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, messege)
    except:
        print("you forget to write your own mail")
    

   