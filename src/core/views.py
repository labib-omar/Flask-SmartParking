from flask import Blueprint, render_template
from flask_login import login_required, current_user

core_bp = Blueprint("core", __name__)

import sys
import os

# Get the path to the directory containing main.py
main_directory = os.path.abspath(os.path.dirname(__file__))
main_directory = os.path.join(main_directory, '..', 'parking_detection')

# Add the main_directory to the module search path
sys.path.append(main_directory)


from parking_detection import main


@core_bp.route("/")
def home():
    empty, img_enc = main.check_spaces()
    return render_template("core/home.html", empty=empty, img_enc=img_enc)


@core_bp.route("/park1")
def park1():
    return render_template("core/park1.html")


@core_bp.route("/park2")
def park2():
    return render_template("core/park2.html")


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