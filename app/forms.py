from flask_wtf import FlaskForm as Form
from wtforms import TextField, PasswordField, StringField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Required


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
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )


class CommandForm(Form):
    command = StringField('Command', [Length(min=1, max=10), Required()])
    response = TextAreaField('Response', [Length(min=1, max=100), Required()])
