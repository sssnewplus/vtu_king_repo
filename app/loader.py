from flask import redirect, url_for
from flask_login import current_user
from functools import wraps


# admin required decorator
def admin_required(f):
    # Decorator to restrict route access to admins only
    @wraps(f)
    def admin_wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return admin_wrapper