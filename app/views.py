from flask import Blueprint, render_template
from flask_login import login_required


# blueprint definition
view = Blueprint("view", __name__)

# 12 main another routes (views)
# 1. dashboard route
@view.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# 2. notification route
@view.route("/notification")
@login_required
def notification():
    return render_template("notification.html")

# 3. profile route
@view.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

# 4. fund wallet route
@view.route("/fund-wallet")
@login_required
def funding():
    return render_template("funding.html")

# 5. buy airtime route
@view.route("/buy-airtime")
@login_required
def buy_airtime():
    return render_template("buy_airtime.html")

# 6. TV subscription route
@view.route("/subscribe-TV")
@login_required
def subscribe_tv():
    return render_template("subscribe_TV.html")

# 7. electricity payment route
@view.route("/pay-electricity")
@login_required
def pay_electricity():
    return render_template("pay_electricity.html")

# 8. exam token generation route
@view.route("/token-generation")
@login_required
def token_generation():
    return render_template("token_generation.html")

# 9. history route
@view.route("/history")
@login_required
def history():
    return render_template("history.html")

# 10. setting route
@view.route("/setting")
@login_required
def setting():
    return render_template("setting.html")

# 11. help route 
@view.route("/help")
@login_required
def user_help():
    return render_template("help.html")

