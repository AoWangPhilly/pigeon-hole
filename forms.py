from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, RadioField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp, ValidationError
from passlib.hash import pbkdf2_sha256

from models import User

class RegisterForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[InputRequired(message="First name is required"), Length(min=2, max=30, message="First name must be between 2 and 30 characters")]
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(message="Last name is required"), Length(min=2, max=30, message="Last name must be between 2 and 30 characters")]
    )
    email = EmailField(
        "Email",
        validators=[InputRequired(message="Email is required"), Email(message="Invalid email format")]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password is required"),
            Length(min=8, max=30, message="Password must be between 8 and 30 characters"),
            Regexp(
                regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])",
                message="Password must contain at least one lowercase letter, one uppercase letter, one numeral, and one special character"
            )
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(message="Please confirm your password"),
            EqualTo('password', message="Passwords must match")
        ]
    )


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already in use")

class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[InputRequired(message="Email is required"), Email(message="Invalid email format")]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(message="Password is required")]
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Invalid email address")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not pbkdf2_sha256.verify(password.data, user.password):
            raise ValidationError("Invalid password")
