from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from .models import Transaction
from . import  db
from .services import transfer_to_granny, buy_airtime


# blueprint definition
view = Blueprint("view", __name__)

# 12 main another routes (views)
# 1. dashboard route
@view.route("/dashboard", methods=['POST', 'GET'])
@login_required
def dashboard():
    if request.method == 'POST':

        # adding fund form
        if 'fund_wallet' in request.form:
            return redirect(url_for( 'funding_wallet'))

        # withdraw fund form
        elif 'withdraw_fund' in request.form:
            return redirect(url_for('view.withdrawing_fund'))

        # services form
        elif 'services' in request.form:
            data = request.form.get('data')
            airtime = request.form.get('airtime')
            tv = request.form.get('tv')
            electricity = request.form.get('electricity')
            exam_token = request.form.get('exam_token')

            if data:
                return redirect(url_for('view.buying_data'))
            elif airtime:
                return redirect(url_for('view.buying_airtime'))
            elif tv:
                return redirect(url_for('view.subscribing_tv'))
            elif electricity:
                return redirect(url_for('view.paying_electricity'))
            elif exam_token:
                return redirect(url_for('view.token_generating'))

    return render_template("main_templates/main_dashboard.html")

# 2. funding wallet route
@view.route("/funding-wallet")
@login_required
def funding_wallet():
    if request.method == 'POST':
        pass
    return render_template("main_templates/funding_wallet.html")

# 3. buying data route
@view.route("/buying-data", methods=['POST', 'GET'])
@login_required
def buying_data():
    if request.method == 'POST':
        user = current_user()
        network = request.form.get('network')
        data_amount = request.form.get('data_amount')
        recipient_phone_number = request.form.get('recipient_phone_number')

        # save the inputs in the session
        session['network'] = network
        session['data_amount'] = data_amount
        session['recipient_phone_number'] = recipient_phone_number

        # checks if inputs are empty
        if not network or not data_amount or not recipient_phone_number:
            flash('all fields are required', category='error')
            return redirect(url_for('buying_data'))

        # checks if user balance is not lower
        if user.balance >= data_amount:
            # withdraw the selling price amount from api wallet (profit + cost)
            # use granny/master wallet to buy the data using cost price (selling_price - profit) -> saving profit
            pass
        else:
            flash('insufficient balance try funding your wallet', category='error')
            return redirect(url_for('buying_data'))

    return render_template("main_templates/buying_data.html")

# 4. buying airtime route
@view.route("/buying-airtime", methods=['POST', 'GET'])
@login_required
def buying_airtime():
    if request.method == 'POST':
        user = current_user()
        network = request.form.get('network')
        airtime_amount = request.form.get('airtime_amount')
        recipient_phone_number = request.form.get('recipient_phone_number')
        pin1 = request.form.get('pin1')
        pin2 = request.form.get('pin2')

        # save the inputs in the session
        session['network'] = network
        session['data_amount'] = airtime_amount
        session['recipient_phone_number'] = recipient_phone_number

        # checks if inputs are empty
        if not network or not airtime_amount or not recipient_phone_number or not pin1 or not pin2:
            flash('all fields are required', category='error')
            return redirect(url_for('buying_airtime'))

        # checks if pin1 == pin2
        if pin1 != pin2:
            flash('PINs do not match', category='error')
            return redirect(url_for('buying_airtime'))

        # checks if pin exist
        if not user.pin:
            flash('you don\'t have a pin, you need to set pin first', category='error')
            return redirect(url_for('auth.set_pin'))

        # checks if user balance is not lower
        if user.balance >= airtime_amount:
            user_wallet_id = user.api_wallet_id
            # withdraw the selling price amount from api wallet (profit + cost) -> transfer to granny
            deducted = transfer_to_granny(sender_wallet_id=user_wallet_id, amount=airtime_amount)
            if deducted["success"]:
                # use granny/master wallet to buy the data using cost price (selling_price - profit) -> saving profit
                airtime_purchase = buy_airtime(amount=airtime_amount, network=network, phone_number=recipient_phone_number)
                if airtime_purchase["success"]:
                    # add new transaction
                    new_transaction = Transaction(user_id=user.id, transaction_type='airtime purchase', amount=airtime_amount, status=True)
                    db.session.add(new_transaction)
                    db.session.commit()
                    flash('airtime purchased successfully', category='success')
                else:
                    flash(f'airtime purchase failed, {airtime_purchase["message"]}', category='error')
        else:
            flash('insufficient balance try funding your wallet', category='error')
            return redirect(url_for('buying_airtime'))

    return render_template("main_templates/buying_airtime.html")

# 5. subscribing tv route
@view.route("/subscribing-tv")
@login_required
def subscribing_tv():
    return render_template("main_templates/subscribe_TV.html")

# 6. paying electricity route
@view.route("/paying-electricity")
@login_required
def paying_electricity():
    return render_template("main_templates/paying_electricity.html")

# 7. generating exam token route
@view.route("/generating-exam-token")
@login_required
def generating_exam_token():
    return render_template("main_templates/generating_exam_token.html")

# 8. profile route
@view.route("/profile")
@login_required
def profile():
    return render_template("main_templates/profile.html")

# 9. history route
@view.route("/history")
@login_required
def history():
    return render_template("main_templates/history.html")

# 10. setting route
@view.route("/setting")
@login_required
def setting():
    return render_template("main_templates/setting.html")

# 11. help route
@view.route("/user-help")
@login_required
def user_help():
    return render_template("main_templates/user_help.html")

# 12. notification route
@view.route("/notification")
@login_required
def notification():
    return render_template("main_templates/notification.html")

