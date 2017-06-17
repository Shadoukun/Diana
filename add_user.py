from app.models import db, User, Admin, Channel, Macro, Quote, FlaskUser
from getpass import getpass
import sys
from flask_bcrypt import generate_password_hash


def main(app):
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if FlaskUser.query.all():
            print('A user already exists! Create another? (y/n):'),
            create = input()
            if create == 'n':
                return

        print('Enter Username: '),
        username = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = FlaskUser(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User added.')

