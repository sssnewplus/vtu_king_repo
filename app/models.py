from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# database models
# 1. user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False) 

    # Relationships
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    referrals = db.relationship('Referral', backref='referrer', lazy=True)

    def __init__(self, name, username, email, password, phone_number):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number

    # method to set name
    def set_name(self, new_name):
        self.name = new_name
        db.session.commit()

    # method to set username
    def set_username(self, new_username):
        self.username = new_username
        db.session.commit()

    # method to set email
    def set_email(self, new_email):
        self.email = new_email
        db.session.commit()

    # method to change email
    def change_email(self, new_email):
        self.email = new_email
        db.session.commit()

    # method to change password
    def set_password(self, new_password):
        self.password = generate_password_hash(new_password)
        db.session.commit() 

    # method to change password
    def change_password(self, old_password, new_password):
        if check_password_hash(self.password, old_password):
            self.password = generate_password_hash(new_password)
            db.session.commit() 
        else:
            return False
        
    # method to check password hash
    def check_password(self, password):
        if check_password_hash(self.password, password):
            return True
        else:
            return False
    
    # method to set phone number
    def set_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number
        db.session.commit()

    # method to change phone number
    def change_phone_number(self, old_phone_number, new_phone_number):
        if User.query.filter_by(phone_number=new_phone_number).first():
            self.phone_number = new_phone_number
            db.session.commit()
            return True
        else:
            return False
        
    # method to get fund user's balance
    def fund_wallet(self, amount):
        self.balance += amount
        db.session.commit()

    # method to withdraw funds from user's balance
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            db.session.commit()
            return True
        else:
            return False

    # method to add transaction
    def add_transaction(self, transaction_id, transaction_type, amount, status):
        transaction = Transaction(transaction_id, self.id, transaction_type, amount, status)
        db.session.add(transaction)
        db.session.commit()
    
    # method to get all transactions for a specific user
    def get_transactions(self):
        return self.transactions
    
    # method to add referral
    @staticmethod
    def add_referral(self, referrer_id, referred_id):
        referral = Referral(referrer_id, referred_id)
        db.session.add(referral)
        db.session.commit()
    
    # method to get all referrals for a specific user
    def get_referrals(self):
        return self.referrals
    
    # methods offered by admin user
    # 1. method to create user (Admin only)
    @staticmethod
    def create_user(name, username, email, password, phone_number, is_admin=False):
        hashed_password = generate_password_hash(password)
        user = User(name=name, username=username, email=email, 
                    password=hashed_password, phone_number=phone_number, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return user

    # Update user details (Admin only)
    def update_user(self, name=None, email=None, phone_number=None, is_admin=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number
        if is_admin is not None:
            self.is_admin = is_admin
        db.session.commit()

    # method to delete user (Admin only)
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
   
    # method to make user an admin
    def make_admin(self):
        self.is_admin = True
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"

# 2. transaction model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(80), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, transaction_id, user_id, transaction_type, amount, status):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.status = status

    # View all transactions (Admin only)
    @staticmethod
    def view_all_transactions():
        return Transaction.query.all()

    # View transactions by user (Admin only)
    def update_transaction_status(self, status):
        self.status = status
        db.session.commit()

    # Delete transaction (Admin only)
    @staticmethod
    def delete_transaction(transaction_id):
        transaction = Transaction.query.get(transaction_id)
        if transaction:
            db.session.delete(transaction)
            db.session.commit()
        return transaction

    def __repr__(self):
        return f"<Transaction {self.transaction_id}, Status: {self.status}>"

# 3. vtu service model
class VTUService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    provider = db.Column(db.String(80), nullable=False)

    def __init__(self, service_name, category, description, price, provider):
        self.service_name = service_name
        self.category = category
        self.description = description
        self.price = price
        self.provider = provider

    def __repr__(self):
        return f"<Service {self.service_name} ({self.category})>"

# 4. airtime/data purchase model
class AirtimeDataPurchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    network_provider = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, transaction_id, phone_number, network_provider, amount, status):
        self.transaction_id = transaction_id
        self.phone_number = phone_number
        self.network_provider = network_provider
        self.amount = amount
        self.status = status

    def __repr__(self):
        return f"<Airtime/Data Purchase for {self.phone_number}>"

# 5. electricity payment model
class ElectricityPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    meter_number = db.Column(db.String(20), nullable=False)
    meter_type = db.Column(db.String(20), nullable=False)
    distributor = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, transaction_id, meter_number, meter_type, distributor, amount, status):
        self.transaction_id = transaction_id
        self.meter_number = meter_number
        self.meter_type = meter_type
        self.distributor = distributor
        self.amount = amount
        self.status = status

    def __repr__(self):
        return f"<Electricity Payment {self.meter_number}>"

# exam token model
class ExamToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, transaction_id, exam_type, token, amount, status):
        self.transaction_id = transaction_id
        self.exam_type = exam_type
        self.token = token
        self.amount = amount
        self.status = status

    def __repr__(self):
        return f"<Exam Token {self.exam_type}>"

# 6. referral model
class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referral_bonus = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, referrer_id, referred_user_id, referral_bonus=0.0):
        self.referrer_id = referrer_id
        self.referred_user_id = referred_user_id
        self.referral_bonus = referral_bonus

    # View all referrals (Admin only)
    @staticmethod
    def view_all_referrals():
        return Referral.query.all()

    # delete a specific referral (Admin only)
    @staticmethod
    def delete_referral(referral_id):
        referral = Referral.query.get(referral_id)
        if referral:
            db.session.delete(referral)
            db.session.commit()
        return referral

    def __repr__(self):
        return f"<Referral by User {self.referrer_id}>"
