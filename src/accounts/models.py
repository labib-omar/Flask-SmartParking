from datetime import datetime
from flask_login import UserMixin
from src import bcrypt, db

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<User email={self.email}>"

from datetime import datetime
from sqlalchemy import DateTime

class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parking_area_id = db.Column(db.Integer, db.ForeignKey("parking_areas.id"), nullable=False)
    reservation_datetime = db.Column(DateTime, nullable=True, default=datetime.now)


    user = db.relationship("User", backref=db.backref("reservations", lazy=True))
    parking_area = db.relationship("ParkingArea", backref=db.backref("reservations", lazy=True))

    def __init__(self, user_id, parking_area_id, reservation_datetime):
        self.user_id = user_id
        self.parking_area_id = parking_area_id
        self.reservation_datetime = reservation_datetime


    def __repr__(self):
        return f"<Reservation user_id={self.user_id}, parking_area_id={self.parking_area_id}, reservation_datetime={self.reservation_datetime}>"


class ParkingArea(db.Model):
    __tablename__ = "parking_areas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    free_spaces = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name, capacity, free_spaces=0):
        self.name = name
        self.capacity = capacity
        self.free_spaces = free_spaces

    def __repr__(self):
        return f"<ParkingArea name={self.name}, capacity={self.capacity}, free_spaces={self.free_spaces}>"
