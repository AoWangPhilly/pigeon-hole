from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    RadioField,
    SelectField,
    DateField,
)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from markupsafe import Markup

from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    Regexp,
    ValidationError,
)

from passlib.hash import pbkdf2_sha256

from models import User, Pigeon, PigeonHierarchy
from constants import NATIONAL_ORG


class RegisterForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[
            InputRequired(message="First name is required"),
            Length(
                min=2, max=30, message="First name must be between 2 and 30 characters"
            ),
        ],
    )
    last_name = StringField(
        "Last Name",
        validators=[
            InputRequired(message="Last name is required"),
            Length(
                min=2, max=30, message="Last name must be between 2 and 30 characters"
            ),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            InputRequired(message="Email is required"),
            Email(message="Invalid email format"),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password is required"),
            Length(
                min=8, max=30, message="Password must be between 8 and 30 characters"
            ),
            Regexp(
                regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])",
                message="Password must contain at least one lowercase letter, one uppercase letter, one numeral, and one special character",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(message="Please confirm your password"),
            EqualTo("password", message="Passwords must match"),
        ],
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already in use")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            InputRequired(message="Email is required"),
            Email(message="Invalid email format"),
        ],
    )
    password = PasswordField(
        "Password", validators=[InputRequired(message="Password is required")]
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Invalid email address")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not pbkdf2_sha256.verify(password.data, user.password):
            raise ValidationError("Invalid password")


class PigeonForm(FlaskForm):
    band_id = StringField(
        "Band ID",
        validators=[
            InputRequired(message="Band ID is required"),
        ],
    )
    name = StringField(
        "Name",
        validators=[
            InputRequired(message="Name is required"),
            Length(min=2, max=30, message="Name must be between 2 and 30 characters"),
        ],
    )

    sex = RadioField(
        "Sex",
        validators=[InputRequired(message="Sex is required")],
        choices=[("cock", "Cock"), ("hen", "Hen")],
    )

    color = SelectField(
        "Color",
        validators=[InputRequired(message="Color is required")],
        choices=[
            (
                "",
                "Choose color",
            ),  # Placeholder, usually not selectable if the field is required
            ("blue", "Blue"),
            ("black", "Black"),
            ("red", "Red"),
            ("yellow", "Yellow"),
            ("white", "White"),
            ("checker", "Checker"),
            ("barred", "Barred"),
            ("pied", "Pied"),
            ("grizzle", "Grizzle"),
            ("t-pattern", "T-pattern"),
            ("dun", "Dun"),
            ("mealy", "Mealy"),
        ],
        default="",  # Sets the default option to the placeholder
    )

    date_of_birth = DateField(
        "Date of Birth", validators=[InputRequired(message="Date of Birth is required")]
    )
    image = FileField(
        "Upload Image",
        validators=[
            FileRequired(message="Image is required"),
            FileAllowed(
                ["jpg", "png", "jpeg", "gif", "webp", "svg", "avif"],
                message="Incorrect file format. Please provide valid .jpg or .png images.",
            ),
        ],
    )


class AddPigeonForm(PigeonForm):
    def validate_band_id(self, band_id):
        try:
            organization, year, club, band = band_id.data.split("-")
        except ValueError:
            raise ValidationError(
                "Invalid band ID format, please use the format: <organization>-<year>-<club>-<band>"
            )

        if organization not in NATIONAL_ORG:
            raise ValidationError(
                f"Invalid organization, please use one of the following: {', '.join(NATIONAL_ORG)} in band ID"
            )

        if len(year) != 4:
            raise ValidationError(
                "Invalid year format, please use a 4-digit year in band ID"
            )

        if year != self.date_of_birth.data.strftime("%Y"):
            raise ValidationError("Year in band ID does not match date of birth")

        if len(club) != 3:
            raise ValidationError(
                "Invalid club format, please use a 3-letter club code in band ID"
            )

        if len(band) != 7:
            raise ValidationError(
                "Invalid band format, please use a 7-digit band number in band ID"
            )

        pigeon = Pigeon.query.filter_by(band_id=band_id.data).first()
        if pigeon:
            raise ValidationError("Band ID already in use")


class EditPigeonForm(PigeonForm):
    def validate_band_id(self, band_id):
        try:
            organization, year, club, band = band_id.data.split("-")
        except ValueError:
            raise ValidationError(
                "Invalid band ID format, please use the format: <organization>-<year>-<club>-<band>"
            )

        if organization not in NATIONAL_ORG:
            raise ValidationError(
                f"Invalid organization, please use one of the following: {', '.join(NATIONAL_ORG)} in band ID"
            )

        if len(year) != 4:
            raise ValidationError(
                "Invalid year format, please use a 4-digit year in band ID"
            )

        if year != self.date_of_birth.data.strftime("%Y"):
            raise ValidationError("Year in band ID does not match date of birth")

        if len(club) != 3:
            raise ValidationError(
                "Invalid club format, please use a 3-letter club code in band ID"
            )

        if len(band) != 7:
            raise ValidationError(
                "Invalid band format, please use a 7-digit band number in band ID"
            )

    image = FileField(
        "Upload Image",
        validators=[
            FileAllowed(
                ["jpg", "png", "jpeg", "gif", "webp", "svg", "avif"],
                message="Incorrect file format. Please provide valid .jpg or .png images.",
            ),
        ],
    )

    def validate_sex(self, sex):
        pigeon = Pigeon.query.filter_by(band_id=self.band_id.data).first()
        if pigeon:
            if pigeon.sex == "cock":
                hierarchy = PigeonHierarchy.query.filter_by(
                    father_id=pigeon._id
                ).first()
            else:
                hierarchy = PigeonHierarchy.query.filter_by(
                    mother_id=pigeon._id
                ).first()

            if hierarchy:
                child_pigeon = Pigeon.query.filter_by(_id=hierarchy.child_id).first()

                if pigeon.sex == "cock" and sex == "hen":
                    raise ValidationError(
                        Markup(
                            f"Pigeon is already father to <a href='/pigeon/{child_pigeon._id}'>{child_pigeon.band_id}</a>"
                        )
                    )
                else:
                    raise ValidationError(
                        Markup(
                            f"Pigeon is already mother to <a href='/pigeon/{child_pigeon._id}'>{child_pigeon.band_id}</a>"
                        )
                    )
