from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
import sys
import os
from src import db
from src.accounts.models import ParkingArea, Reservation
from datetime import datetime


core_bp = Blueprint("core", __name__)


# Get the path to the directory containing main.py
main_directory = os.path.abspath(os.path.dirname(__file__))
main_directory = os.path.join(main_directory, '..', 'parking_detection')

# Add the main_directory to the module search path
sys.path.append(main_directory)

from parking_detection import main


def update_parking_area_spaces():
    parking_area = ParkingArea.query.get(1)  # Retrieve the desired ParkingArea object
    free_spaces = main.check_spaces()  # Get the number of free spaces using checkspaces()
    parking_area.free_spaces = free_spaces  # Update the number of free spaces
    db.session.commit()  # Save the changes to the database


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


@core_bp.route("/reserve/confirm", methods=["POST"])
@login_required
def reserve_confirm():
    if request.method == "POST":
        # Create a new reservation for the current user with the current date and time
        reservation = Reservation(user_id=current_user.id, reservation_datetime=datetime.now(), parking_area_id=1)
        db.session.add(reservation)
        db.session.commit()

        return render_template("core/reserve_success.html")


@core_bp.route("/park2")
def park2():
    return render_template("core/park2.html")


@core_bp.route("/dashboard")
@login_required
def dash():
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template("core/dashboard.html", reservations=user_reservations)


@core_bp.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        return render_template("core/admin.html")
    else:
        return render_template("errors/401.html")