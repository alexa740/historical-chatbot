import smtplib
import random

OTP_STORE = {}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    OTP_STORE[email] = otp
    
    sender_email = "infohistoric2@gmail.com"
    sender_password = "jqcgddlbhgibcstj"
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    message = f"Subject: Your OTP Code\n\nYour OTP code is {otp}. Please enter this code to verify your email."
    server.sendmail(sender_email, email, message)
    server.quit()

    return otp

def verify_otp(email, user_otp):
    return OTP_STORE.get(email) == user_otp