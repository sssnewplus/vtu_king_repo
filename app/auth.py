from flask import Blueprint, flash, request, render_template, session, redirect, url_for
from app.validators import validate_email, validate_password, validate_phone_number
from .models import User
from flask_login import login_required, login_user, logout_user, current_user
from .import db
from .validators import send_email_otp, generate_otp, verify_otp
from .services import create_wallet_with_retries

# blueprint definition
auth = Blueprint("auth", __name__)

# welcome route
@auth.route("/", methods=['POST', 'GET'])
def welcome():
    # username = session['username']
    # user = User.query.filter_by(username=username)
    # if username:
    #     if user:
    #         return render_template("auth_templates/welcome.html")
    #     return redirect(url_for('auth.login'))
    return render_template("auth_templates/welcome.html")


# six authentication routes
# 1 pre authentication route
@auth.route("/pre-auth", methods=['POST', 'GET'])
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

        # lets store form data in a session
        session['name'] = name
        session['username'] = username
        session['email'] = email
        session['phone_number'] = phone_number
        session['referral_username'] = referral_username

        user_username = User.query.filter_by(email=username).first()
        user_email = User.query.filter_by(username=email).first()

        # checks if the input field are empty
        if not name or not username or not email or not phone_number or not password1 or not password2:
            flash("All fields are required except referral", category="error")
            return redirect(url_for('auth.sign_up'))

        # check if username or email already exists
        elif user_username:
            flash("Username already exists", category="error")
            return redirect(url_for('auth.sign_up'))

        elif user_email:
            flash("Email already exists", category="error")
            return redirect(url_for('auth.sign_up'))

        # check if name is valid
        elif not name.isalpha() or not name.strip():
            flash("Name must contain only alphabetic characters", category="error")
            return redirect(url_for('auth.sign_up'))
        elif len(name) < 3:
            flash("Name must be at least 3 characters long", category="error")
            return redirect(url_for('auth.sign_up'))

        # check if username is valid
        elif not username.isalnum() or not username.strip():
            flash("Username must contain only alphanumeric characters", category="error")
            return redirect(url_for('auth.sign_up'))
        elif len(username) < 5:
            flash("Username must be at least 5 characters long", category="error")
            return redirect(url_for('auth.sign_up'))

        # check if email is valid
        elif not validate_email(email):
            flash("Invalid email address", category="error")
            return redirect(url_for('auth.sign_up'))

        # check if phone number is valid
        elif not validate_phone_number(phone_number):
            flash("Invalid phone number format, ", category="error")
            return redirect(url_for('auth.sign_up'))

        # check if passwords match
        elif password1 != password2:
            flash("Passwords do not match", category="error")
            return redirect(url_for('auth.sign_up'))
        elif len(password1) < 8:
            flash("Password must be at least 8 characters long", category="error")
            return redirect(url_for('auth.sign_up'))
        elif not validate_password(password2):
            flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character", category="error")
            return redirect(url_for('auth.sign_up'))
        else:
            # checks if referral exists in users
            referral = User.query.filter_by(username=referral_username).first()
            if not referral:
                flash("Referral username doesn't exist!", category="info")
                # return redirect(url_for('auth.sign_up'))

            referral_username = referral_username

            # create a new user
            new_user = User()
            new_user.set_name(name)
            new_user.set_username(username)
            new_user.set_email(email)
            new_user.set_password(password2)
            new_user.set_phone_number(phone_number)
            new_user.referred_by = referral_username
            db.session.add(new_user)
            db.session.commit()

            # create api wallet for the user
            api_wallet = create_wallet_with_retries(new_user)
            if api_wallet["success"]:
                # save the api wallet id to the database
                new_user.api_wallet_id = api_wallet["wallet_id"]
                db.session.commit()

            # clear the session data
            session.pop('name', None)
            session.pop('username', None)
            session.pop('email', None)
            session.pop('phone_number', None)
            session.pop('referral_username', None)

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

        # let add form data to the session
        session['username'] = username

        # check if the fields are empty
        if not username or not password:
            flash('All fields are required', category="error")
            return redirect(url_for('auth.login'))

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
                # clear the session data
                session.pop('username', None)
                login_user(user_with_email)
                return render_template("main_templates/main_dashboard.html")
        else:
            flash('Invalid username or password', category="error")
            return redirect(url_for('auth.login'))
    return render_template("auth_templates/login.html")

# 4 logout route (additional route ( it's non-template rendering ))
@auth.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    session.clear()
    return render_template("auth_templates/pre_auth.html")

# 5 password forgotten route (find account, request otp and reset password)
@auth.route("/reset-password", methods=['POST', 'GET'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username_or_email')
        session['username'] = username

        user_by_email = User.query.filter_by(email=username).first()
        user_by_username = User.query.filter_by(username=username).first()


        if not username:
            flash('enter your username or email', category='error')
            return redirect(url_for('auth.reset_password'))

        # first form to find the account using email or username then request for otp
        if 'username_submit_btn' in request.form:
            if user_by_email:
                otp = generate_otp(5)  # generate otp
                session['otp'] = otp  # save it to session
                send_email_otp(user_by_email.email, otp)  # send it to user email
                flash('otp sent to your email', category='success')
            elif user_by_username:
                otp = generate_otp(5)  # generate otp
                session['otp'] = otp  # save it to session
                send_email_otp(user_by_email.email, otp)  # send it to user email
                flash('otp sent to your email', category='success')
            elif not user_by_username:
                flash("account with this username doesn't exist", category='error')
                return redirect(url_for('auth.reset_password'))
            elif not user_by_email:
                flash("account with this email doesn't exist", category='error')
                return redirect(url_for('auth.reset_password'))

            user_otp = request.form.get('otp')
            session['user_otp'] = user_otp

            if verify_otp(user_otp):
                flash('otp verified', category='success')
                return redirect(url_for('auth.reset_password'))
            else:
                flash('invalid otp', category='error')
                return redirect(url_for('auth.reset_password'))

        # third form to reset the password
        elif 'password_submit_btn' in request.form:
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            if password1 == password2:
                if user_by_email:
                    user_by_email.set_password(password2)
                    db.session.commit()
                    flash('Password reset successful, proceed to login', category="success")
                    session.pop('username', None)
                    session.pop('otp', None)
                    session.pop('user_otp', None)
                    return redirect(url_for('auth.login'))
                elif user_by_username:
                    user_by_username.set_password(password2)
                    db.session.commit()
                    flash('Password reset successful, proceed to login', category="success")
                    session.pop('username', None)
                    session.pop('otp', None)
                    session.pop('user_otp', None)
                    return redirect(url_for('auth.login'))
            else:
                    flash('Passwords do not match', category="error")
                    return redirect(url_for('auth.reset_password'))

    return render_template("auth_templates/reset_password.html")


# 6 change password route (if already login)
@auth.route("/change-password", methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == 'POST':

        user = current_user()
        user_old_password = request.form.get('old_password')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        if not user_old_password or not new_password1 or not new_password2:
            flash('All fields are required', category='error')
            return redirect(url_for('auth.change_password'))

        if new_password1 != new_password2:
            flash('New passwords do not match', category='error')
            return redirect(url_for('auth.change_password'))

        user.change_password(user_old_password, new_password2)
        flash('Password changed successfully', category='success')
        return redirect(url_for('auth.login'))

    return render_template("auth_templates/change_password.html")


 # 6 change pin route
@auth.route("/change-pin", methods=['POST', 'GET'])
@login_required
def change_pin():
    if request.method == 'POST':
        user = current_user()
        old_pin = request.form.get('old_pin')
        new_pin_1 = request.form.get('new_pin1')
        new_pin_2 = request.form.get('new_pin2')

        session['old_pin'] = old_pin
        session['new_pin_1'] = new_pin_1
        session['new_pin_2'] = new_pin_2

        if user.pin != old_pin:
            flash('Incorrect old pin', category='error')
            return redirect(url_for('auth.change_pin'))

        if new_pin_1 != new_pin_2:
            flash('New PINs do not match', category='error')
            return redirect(url_for('auth.change_pin'))

        user.change_pin(old_pin, new_pin_2)
        flash('PIN changed successfully', category='success')
        return redirect(url_for('auth.login'))
    
    return render_template("auth_templates/change_pin.html")