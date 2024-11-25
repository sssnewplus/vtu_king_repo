import re

# validators functions
# 1. func to validate email
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

# 2. func to validate phone number
def validate_phone_number(phone_number):
    pattern = r'^\+\d{1,3}-\d{1,3}-\d{1,4}-\d{1,4}$'
    return bool(re.match(pattern, phone_number))

# 3. func to validate password
def validate_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))
