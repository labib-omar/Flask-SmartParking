from flask import Blueprint, render_template
from flask_login import login_required, current_user

core_bp = Blueprint("core", __name__)


@core_bp.route("/home")
def home():
    return render_template("core/home.html")

@core_bp.route("/dashboard")
@login_required
def dash():
    return render_template("core/dashboard.html")


@core_bp.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        return render_template("core/admin.html")
    else:
        return render_template("errors/401.html")