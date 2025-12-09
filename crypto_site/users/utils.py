from random import randint
import smtplib
from dotenv import load_dotenv
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

def onetime_code():
    code = ""
    for _ in range(4):
        num = randint(0, 9)
        code += str(num)
    
    return code


def send_email(Receiver, one_time_code):
    
    sender = os.getenv("code_sender_email")
    receiver = Receiver
    password = os.getenv("app_password")
    subject = "Khurmax, One-time code"
    body = f"Here is your one-time code:\n {one_time_code}"

    messege = f"""From: {sender}
    To: {receiver}pyth
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
    

   