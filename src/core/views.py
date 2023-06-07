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

from src import db
from src.accounts.models import ParkingArea

def update_parking_area_spaces():
    parking_area = ParkingArea.query.get(1)  # Retrieve the desired ParkingArea object
    free_spaces = main.check_spaces()  # Get the number of free spaces using checkspaces()
    parking_area.free_spaces = free_spaces  # Update the number of free spaces
    db.session.commit()  # Save the changes to the database

from parking_detection import main


@core_bp.route("/")
def home():
    return render_template("core/home.html")


@core_bp.route("/park1")
def park1():
    update_parking_area_spaces()
    return render_template("core/park1.html", name = ParkingArea.query.get(1).name, available_spaces_park1=ParkingArea.query.get(1).free_spaces)

@core_bp.route("/reserve")
@login_required
def reserve():
    return render_template("core/reserve.html", name = ParkingArea.query.get(1).name)


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