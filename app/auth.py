from flask import Blueprint, flash, request, render_template
from app.validators import validate_email, validate_password, validate_phone_number
from .models import User
from flask_login import login_required, login_user, logout_user
from .import db

# blueprint definition
auth = Blueprint("auth", __name__)

# six authentication routes
# 1 pre authentication route
@auth.route("/")
def pre_auth():
    return render_template("auth_templates/pre_auth.html")

# 2 sign up route
@auth.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':

        # grab the user data
        name = request.form.get("full_name")
        username = request.form.get("username")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        referral_username = request.form.get("referral_username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # check if username or email already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", category="error")
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category="error")

        # check if name is valid
        if not name.isalpha() or not name.strip():
            flash("Name must contain only alphabetic characters", category="error")
        elif len(name) < 3:
            flash("Name must be at least 3 characters long", category="error")

        # check if username is valid
        if not username.isalnum() or not username.strip():
            flash("Username must contain only alphanumeric characters", category="error")
        elif len(username) < 5:
            flash("Username must be at least 5 characters long", category="error")

        # check if email is valid
        if not validate_email(email):
            flash("Invalid email address", category="error")

        # check if phone number is valid
        if not validate_phone_number(phone_number):
            flash("Invalid phone number format, ", category="error")

        # check if passwords match
        if password1 != password2:
            flash("Passwords do not match", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long", category="error")
        elif not validate_password(password2):
            flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character", category="error")
        else:

            # checks if referral exists in users
            referral = User.query.filter_by(username=referral_username).first()
            if not referral:
                flash("Referral username doesn't exist!", category="error")
                referral_username = None
            else:
                referral_username = referral_username

            # create a new user
            new_user = User()
            new_user.set_name(name)
            new_user.set_username(username)
            new_user.set_email(email)
            new_user.set_password(password2)
            new_user.set_phone_number(phone_number)
            new_user.set_referral_username(referral_username)
            db.session.add(new_user)
            db.session.commit()

            # login the user after signing up
            login_user(new_user)
            return render_template("main_templates/main_dashboard.html")
    return render_template("auth_templates/sign_up.html")

# 3 login route
@auth.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # grab the form data
        username = request.form.get('username_or_email')
        password = request.form.get('password')

        # check if user exists
        # login with username and password
        user_with_username = User.query.filter_by(username=username).first()
        if user_with_username and user_with_username.check_password(password):
            flash('Login successful', category="success")
            login_user(user_with_username)
            return render_template("main_templates/main_dashboard.html")

        # login with email and password
        elif not user_with_username:
            user_with_email = User.query.filter_by(email=username).first()
            if user_with_email and user_with_email.check_password(password):
                flash('Login successful', category="success")
                login_user(user_with_email)
                return render_template("main_templates/main_dashboard.html")
        else:
            flash('Invalid username or password', category="error")
    return render_template("auth_templates/login.html")

# logout route (additional route ( it's non-template rendering ))
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("auth_templates/pre_auth.html")

# 4 password forgotten route (find account and request otp)
@auth.route("/find-account")
def find_account():
    return render_template("auth_templates/find_account.html")

# 5 otp validation route
@auth.route("/confirm-otp")
def confirm_otp():
    return render_template("auth_templates/confirm_otp.html")

# 6 changing with new password route
@auth.route("/create-new-password")
def create_new_password():
    if request.method == 'POST':
        # grab the form data
        username = request.form.get('username_or_email')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')

        # check if user exists
        user = User.query.filter_by(username=username).first()
        if user:
            if password1 == password2:
                user.set_password(password2)
                db.session.commit()
                flash('Password reset successful', category="success")
            else:
                flash('Passwords do not match', category="error")
        else:
            flash('Invalid username or email', category="error")
    return render_template("auth_templates/create_new_password.html")

