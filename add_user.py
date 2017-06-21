from app import db
from app.models import User, Admin, Channel, Macro, Quote, FlaskUser
from getpass import getpass
import sys
from flask_bcrypt import generate_password_hash


def add_user(app):
    """Main entry point for script."""
    with app.app_context():
        if FlaskUser.query.all():
            return

        print('Enter Username: '),
        username = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = FlaskUser(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User added.')

