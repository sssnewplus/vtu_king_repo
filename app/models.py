from app import db
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# database models
# 1. user model
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) # store user id 
    name = db.Column(db.String(80), nullable=False) # store user full name 
    username = db.Column(db.String(80), unique=True, nullable=False) # store user username
    email = db.Column(db.String(120), unique=True, nullable=False) # store user email
    password = db.Column(db.String(255), nullable=False) # store user hashed password
    phone_number = db.Column(db.String(15), nullable=False) # store user phone number
    balance = db.Column(db.Float, default=0.0) # store user balance
    api_wallet_id = db.Column(db.String(200)) # store id of api wallet
    api_wallet_account_number = db.Column(db.String(200)) # store api wallet account number
    pin = db.Column(db.String(4), nullable=False, default='1111') # store user pin for transaction
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) # store time when the user was created
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc)) # store time when the user was updated
    is_admin = db.Column(db.Boolean, default=False) # store whether the user is an admin user or not
    referred_by = db.Column(db.String(80), nullable=True) # store the referrer of the user

    # Relationships (one user object can have many transactions, 1 -> many)
    transactions = db.relationship('Transaction', primaryjoin="User.id == Transaction.user_id", backref='user', lazy=True) # store the transactions belong to a user
    
    # Relationships (one user object can have many transactions, 1 -> many)
    referrals = db.relationship('Referral', foreign_keys='Referral.referrer_id', backref='referrer', lazy=True) # store the referrals that the user referred

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

    # method to set password
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
        if User.query.filter_by(phone_number=old_phone_number).first():
            self.phone_number = new_phone_number
            db.session.commit()
            return True
        else:
            return False

    # method to set pin
    def set_pin(self, new_pin):
        self.pin = new_pin
        db.session.commit()

    # method to change pin
    def change_pin(self, old_pin, new_pin):
        if self.pin == old_pin:
            self.pin = new_pin
            db.session.commit()
            return True

    # method to reset pin
    def reset_pin(self):
        self.pin = None

        
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
    
    # method to get all transactions for a specific user
    def get_transactions(self):
        return self.transactions

    # method to get all referrals for a specific user
    def get_referrals(self):
        return self.referrals
    
    # method to soft delete user
    def soft_delete_user(self):
        user = User.query.get(self.id)
        if user:
            user.deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return {"success": True, "message": "User soft deleted"}
        return {"success": False, "message": "User not found"}


    # methods offered by admin user
    # 1. method to create user (Admin only)
    @staticmethod
    def create_user(name, username, email, password, phone_number):
        hashed_password = generate_password_hash(password)
        user = User()
        user.set_name(name)
        user.set_username(username)
        user.set_email(email)
        user.set_password(hashed_password)
        user.set_phone_number(phone_number)
        db.session.add(user)
        db.session.commit()
        db.session.add(user)
        db.session.commit()
        return user

    # Update user details (Admin only)
    @staticmethod
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
    @staticmethod
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
   
    # method to make user an admin
    @staticmethod
    def make_admin(self):
        self.is_admin = True
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>, referred by {self.referred_by}"

# 2. transaction model
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    # transaction_id = db.Column(db.String(80), unique=True, nullable=False)
    # foreign key (one transaction can have one id of user, 1 -> 1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_transactions_user_id'), nullable=False)
    api_transaction_id = db.Column(db.String(100), nullable=True)  # Store API transaction ID
    transaction_type = db.Column(db.String(50), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # View all transactions (Admin only)
    @staticmethod
    def view_all_transactions():
        return Transaction.query.all()

    # Update transaction status (Admin only)
    @staticmethod
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
    __tablename__ = 'vtu_services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(80), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    provider = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return f"<Service {self.service_name} ({self.category})>"

# 4. airtime/data purchase model
class AirtimeDataPurchase(db.Model):
    __tablename__ = 'airtime_or_data_purchases'
    id = db.Column(db.Integer, primary_key=True)
    # foreign key (one data or airtime purchase can have one transaction id, 1 -> 1)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id', name='fk_airtime_or_data_purchase_transaction_id'), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    network_provider = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


    def __repr__(self):
        return f"<Airtime/Data Purchase for {self.phone_number}>"

# 5. electricity payment model
class ElectricityPayment(db.Model):
    __tablename__ = 'electricity_payments'
    id = db.Column(db.Integer, primary_key=True)
    # foreign key (one electric payment can have one transaction id, 1 -> 1)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id', name='fk_electricity_payments_transaction_id'), nullable=False)
    meter_number = db.Column(db.String(20), nullable=False)
    meter_type = db.Column(db.String(20), nullable=False)
    distributor = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Electricity Payment {self.meter_number}>"

# exam token model
class ExamToken(db.Model):
    __tablename__ = 'exam_tokens'
    id = db.Column(db.Integer, primary_key=True)
    # foreign key (one exam token generation can have one transaction id, 1 -> 1)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id', name='fk_exam_tokens_transaction_id'), nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


    def __repr__(self):
        return f"<Exam Token {self.exam_type}>"

# 6. referral model
class Referral(db.Model):
    __tablename__ ='referrals'
    id = db.Column(db.Integer, primary_key=True)
    # foreign key (one referral can have one referrer id (user id), 1 -> 1)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_referrals_referred_user_id'), nullable=False)
    referral_bonus = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

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
