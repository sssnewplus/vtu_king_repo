import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import session
import time

# validators functions
# 1. func to validate email
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

# 2. func to validate phone number
def validate_phone_number(phone_number):
    pattern = r'^\d{11}$'
    return bool(re.match(pattern, phone_number))

# 3. func to validate password
def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

# 4. func to generate otp
def generate_otp(length):
    otp = ''.join(random.choices('0123456789', k=length))
    return otp

# 5. func to send otp
def send_email_otp(to_email, otp):
    sender_email = "__vtuservices@gmial.com"
    sender_password = "123456789"

    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}\n\nThis code is valid for 10 minutes."

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return "OTP sent successfully!"
    except Exception as e:
        return f"Failed to send OTP: {str(e)}"
    pass

# 6. func to verify otp
def verify_otp(user_otp):
    if 'otp' in session and session['otp'] == user_otp:
        if time.time() < session.get('otp_expiry', 0):  # Check expiry
            return True
        else:
            return False  # Expired OTP
    return False

