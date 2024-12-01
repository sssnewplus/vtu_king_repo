from flask import Blueprint, render_template
from flask_login import login_required
from .loader import admin_required
# from .models import User

admin = Blueprint("admin", __name__)

# admin route
@admin.route("/admin-dashboard")
@login_required
@admin_required
def admin_dashboard():
    return render_template("admin_dashboard.html")

# manage users route
@admin.route("/manage-users")
@login_required
@admin_required
def manage_users():
    # users = User.query.all()
    return render_template("manage_users.html")