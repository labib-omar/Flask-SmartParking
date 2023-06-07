from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
import sys
import os
from src import db
from src.accounts.models import ParkingArea, Reservation
from datetime import datetime, timedelta


core_bp = Blueprint("core", __name__)


# Get the path to the directory containing main.py
main_directory = os.path.abspath(os.path.dirname(__file__))
main_directory = os.path.join(main_directory, '..', 'parking_detection')

# Add the main_directory to the module search path
sys.path.append(main_directory)

from parking_detection import main


@core_bp.route("/")
def home():
    return render_template("core/home.html")


def update_parking_area_spaces(area_id):
    parking_area = ParkingArea.query.get(area_id)  # Retrieve the desired ParkingArea object
    free_spaces = main.check_spaces()  # Get the number of free spaces using checkspaces()
    reserved = 0
    for reservation in parking_area.reservations:
        if reservation.active:
            reserved = reserved + 1
    parking_area.free_spaces = free_spaces - reserved  # Update the number of free spaces
    db.session.commit()  # Save the changes to the database



@core_bp.route("/park1")
@login_required
def park1():
    parking_area_id = 1
    update_parking_area_spaces(parking_area_id)
    return render_template("core/park1.html", name=ParkingArea.query.get(parking_area_id).name, available_spaces_park=ParkingArea.query.get(parking_area_id).free_spaces, parking_area_id=parking_area_id)


@core_bp.route("/park2")
@login_required
def park2():
    parking_area_id = 2
    update_parking_area_spaces(parking_area_id)
    return render_template("core/park2.html", name=ParkingArea.query.get(parking_area_id).name, available_spaces_park=ParkingArea.query.get(parking_area_id).free_spaces, parking_area_id=parking_area_id)


@core_bp.route("/reserve")
@login_required
def reserve():
    parking_area_id = request.args.get('parking_area_id')
    if parking_area_id is None:
        # Redirect if parking_area_id is not provided
        return render_template("errors/404.html")

    # Pass the parking_area_id to the template
    return render_template("core/reserve.html", parking_area_id=parking_area_id)


@core_bp.route("/reserve_confirm/<int:parking_area_id>", methods=["POST"])
@login_required
def reserve_confirm(parking_area_id):
    if request.method == "POST":
        # Check if the user has another reservation within the last hour
        last_hour = datetime.now() - timedelta(hours=1)
        has_previous_reservation = Reservation.query.filter(
            Reservation.user_id == current_user.id,
            Reservation.active == True,
            Reservation.reservation_datetime >= last_hour
        ).first()

        if has_previous_reservation:
            flash("You already have a reservation within the last hour.", "warning")
            return redirect(url_for("core.park" + str(parking_area_id)))

        # Create a new reservation for the current user with the current date and time and the specified parking area
        reservation = Reservation(
            user_id=current_user.id,
            reservation_datetime=datetime.now(),
            parking_area_id=parking_area_id
        )
        db.session.add(reservation)
        db.session.commit()

        return render_template("core/reserve_success.html", name = ParkingArea.query.get(parking_area_id).name)






@core_bp.route("/dashboard")
@login_required
def dash():
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template("core/dashboard.html", reservations=user_reservations)

@core_bp.route("/cancel_reservation", methods=["POST"])
@login_required
def cancel_reservation():
    reservation_id = request.form.get("reservationId")

    # Retrieve the reservation from the database
    reservation = Reservation.query.get(reservation_id)

    if reservation:
        # Update the reservation's active status to False
        reservation.active = False
        db.session.commit()
        flash("Reservation cancelled successfully", "success")
        return "Reservation cancelled successfully", 200
    else:
        flash("Reservation not found", "danger")
        return "Reservation not found", 404

@core_bp.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        return render_template("core/admin.html")
    else:
        return render_template("errors/401.html")