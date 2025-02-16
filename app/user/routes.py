from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.user import bp

@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    print("sa")
    if current_user:
        return render_template('user/dashboard.html'), 200
    else:
        return redirect(url_for("auth.login"))