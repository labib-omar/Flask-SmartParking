from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
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


@core_bp.route("/add_parking", methods=["GET", "POST"])
@login_required
def add_parking():
    if current_user.is_admin:
        if request.method == "POST":
            name = request.form.get("name")
            capacity = int(request.form.get("capacity"))
            map_link = request.form.get("map_link")
            detection_method = request.form.get("detection_method")
            video_path = request.form.get("video_path")

            # Process the form data and add the parking area to the database
            parking_area = ParkingArea(name=name, capacity=capacity, map_link=map_link, detection_method=detection_method, video_path=video_path)
            db.session.add(parking_area)
            db.session.commit()

            flash("Parking area added successfully", "success")
            return redirect(url_for("core.dash"))

        return render_template("core/addParking.html")

    return render_template("errors/401.html")



@core_bp.route("/")
def home():
    parking_areas = ParkingArea.query.all()
    return render_template("core/home.html", parking_areas=parking_areas)

def update_parking_area_spaces(area_id):
    parking_area = ParkingArea.query.get(area_id)  # Retrieve the desired ParkingArea object
    free_spaces = main.check_spaces()  # Get the number of free spaces using checkspaces()
    reserved = 0
    for reservation in ParkingArea.query.get(area_id).reservations:
        if reservation.active:
            reserved = reserved + 1
    parking_area.free_spaces = free_spaces - reserved  # Update the number of free spaces
    db.session.commit()  # Save the changes to the database


""" import threading

# Global variable to hold the value
empty = 0
img_enc = ""

# Flag variable to control the thread
run_thread = False


@core_bp.route("/get_empty", methods=["GET"])
def get_empty():
    global empty, img_enc
    empty, img_enc = main.check_spaces()
    return jsonify(value=empty, img_enc=img_enc)
 """

""" @core_bp.route("/parkAdmin")
@login_required
def parkAdmin():
    global run_thread
    if current_user.is_admin:

        # Start the thread to update the empty value
        update_thread = threading.Thread(target=get_empty)
        update_thread.start()

        return render_template("core/parkAdmin.html")
    run_thread = False
    return render_template("errors/401.html")
 """

""" @core_bp.route("/park1")
@login_required
def park1():
    parking_area_id = 1
    update_parking_area_spaces(parking_area_id)
    return render_template("core/park1.html", name=ParkingArea.query.get(parking_area_id).name, available_spaces_park=ParkingArea.query.get(parking_area_id).free_spaces, parking_area_id=parking_area_id)
 """
@core_bp.route("/park<int:parking_area_id>")
@login_required
def park(parking_area_id):
    parking_area = ParkingArea.query.get(parking_area_id)
    update_parking_area_spaces(parking_area_id)
    return render_template("core/park.html", parking_area=parking_area)


""" 
@core_bp.route("/park2")
@login_required
def park2():
    parking_area_id = 2
    update_parking_area_spaces(parking_area_id)
    return render_template("core/park2.html", name=ParkingArea.query.get(parking_area_id).name, available_spaces_park=ParkingArea.query.get(parking_area_id).free_spaces, parking_area_id=parking_area_id)

 """
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
            return redirect(url_for("core.park", parking_area_id=parking_area_id))

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
    global run_thread
    run_thread = False
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    if current_user.is_admin:
        user_reservations = Reservation.query.all()
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

""" @core_bp.route("/admin")
@login_required
def admin():
    if current_user.is_admin:
        return render_template("core/admin.html")
    else:
        return render_template("errors/401.html") """