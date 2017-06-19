from flask_wtf import FlaskForm as Form
from wtforms import TextField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Required
from flask_bcrypt import check_password_hash

from app.models import FlaskUser


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
         EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = FlaskUser.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class CommandForm(Form):
    command = StringField('Command', [Length(min=1, max=10), Required()])
    response = TextAreaField('Response', [Length(min=1, max=100), Required()])
