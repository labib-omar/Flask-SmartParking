from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sys
import os
from src import db
from src.accounts.models import ParkingArea, Reservation
from datetime import datetime, timedelta

# Create blueprint
core_bp = Blueprint("core", __name__)

# Add path to the module search path
main_directory = os.path.abspath(os.path.dirname(__file__))
main_directory = os.path.join(main_directory, '..', 'parking_detection')
sys.path.append(main_directory)

# Import main.py from parking_detection
from parking_detection import main


# Route: Add Parking
@core_bp.route("/add_parking", methods=["GET", "POST"])
@login_required
def add_parking():
    if current_user.is_admin:
        if request.method == "POST":
            # Process the form data and add the parking area to the database
            parking_area = ParkingArea(
                name=request.form.get("name"),
                capacity=int(request.form.get("capacity")),
                map_link=request.form.get("map_link"),
                detection_method=request.form.get("detection_method"),
                video_path=request.form.get("video_path")
            )
            db.session.add(parking_area)
            db.session.commit()

            flash("Parking area added successfully", "success")
            return redirect(url_for("core.dash"))

        return render_template("core/addParking.html")

    return render_template("errors/401.html")


# Route: Home
@core_bp.route("/")
def home():
    parking_areas = ParkingArea.query.all()
    return render_template("core/home.html", parking_areas=parking_areas)


# Helper function: Update parking area spaces
def update_parking_area_spaces(area_id):
    parking_area = ParkingArea.query.get(area_id)
    free_spaces = parking_area.capacity

    if parking_area.detection_method == "OpenCV":
        free_spaces = main.check_spaces()
    elif parking_area.detection_method == "YoloV7":
        free_spaces = 100
    
    reserved = 0
    for reservation in parking_area.reservations:
        if reservation.active:
            reserved += 1
    parking_area.free_spaces = free_spaces - reserved
    db.session.commit()


# Route: Park
@core_bp.route("/park<int:parking_area_id>")
@login_required
def park(parking_area_id):
    parking_area = ParkingArea.query.get(parking_area_id)
    update_parking_area_spaces(parking_area_id)
    return render_template("core/park.html", parking_area=parking_area)


# Route: Reserve
@core_bp.route("/reserve")
@login_required
def reserve():
    parking_area_id = request.args.get('parking_area_id')
    if parking_area_id is None:
        return render_template("errors/404.html")

    return render_template("core/reserve.html", name=ParkingArea.query.get(parking_area_id).name, parking_area_id=parking_area_id)


# Route: Confirm Reservation
@core_bp.route("/reserve_confirm/<int:parking_area_id>", methods=["POST"])
@login_required
def reserve_confirm(parking_area_id):
    if request.method == "POST":
        last_hour = datetime.now() - timedelta(hours=1)
        has_previous_reservation = Reservation.query.filter(
            Reservation.user_id == current_user.id,
            Reservation.active == True,
            Reservation.reservation_datetime >= last_hour
        ).first()

        if has_previous_reservation:
            flash("You already have a reservation within the last hour.", "warning")
            return redirect(url_for("core.park", parking_area_id=parking_area_id))

        reservation = Reservation(
            user_id=current_user.id,
            reservation_datetime=datetime.now(),
            parking_area_id=parking_area_id
        )
        db.session.add(reservation)
        db.session.commit()

        return render_template("core/reserve_success.html", name=ParkingArea.query.get(parking_area_id).name)


# Route: Dashboard
@core_bp.route("/dashboard")
@login_required
def dash():
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    if current_user.is_admin:
        user_reservations = Reservation.query.all()
    return render_template("core/dashboard.html", reservations=user_reservations)


# Route: Cancel Reservation
@core_bp.route("/cancel_reservation", methods=["POST"])
@login_required
def cancel_reservation():
    reservation_id = request.form.get("reservationId")
    reservation = Reservation.query.get(reservation_id)

    if reservation:
        reservation.active = False
        db.session.commit()
        flash("Reservation cancelled successfully", "success")
        return "Reservation cancelled successfully", 200
    else:
        flash("Reservation not found", "danger")
        return "Reservation not found", 404
