import getpass
import unittest

from flask.cli import FlaskGroup

from src import app, db
from src.accounts.models import *

cli = FlaskGroup(app)


@cli.command("test")
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@cli.command("create_admin")
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        print(f"Admin with email {email} created successfully!")
    except Exception:
        print("Couldn't create admin user.")


@cli.command("create_parking_area")
def create_parking_area():
    """Creates a parking area."""
    name = input("Enter parking area name: ")
    capacity = int(input("Enter parking area capacity: "))
    try:
        parking_area = ParkingArea(name=name, capacity=capacity, free_spaces=capacity)
        db.session.add(parking_area)
        db.session.commit()
        print(f"Parking area {name} created successfully!")
    except Exception as e:
        print(f"Couldn't create parking area. Error: {str(e)}")



if __name__ == "__main__":
    cli()
