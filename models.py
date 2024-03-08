from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True


db = SQLAlchemy()


@dataclass
class User(db.Model):
    _id: int
    email: str
    password: str
    name: str

    __tablename__ = "users"
    _id = db.Column("id", db.Integer, primary_key=True)
    email = db.Column("email", db.String(100), unique=True, nullable=False)
    password = db.Column("password", db.String(100), nullable=False)
    name = db.Column("name", db.String(100), nullable=False)

    def __str__(self) -> str:
        return f"<User: {self.email} | Name: {self.name}>"


@dataclass
class Pigeon(db.Model):
    _id: int
    user_id: int
    band_id: str
    name: str
    sex: str
    color: str
    date_of_birth: str
    image_url: str

    __tablename__ = "pigeons"
    _id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    band_id = db.Column("band_id", db.String(100), unique=True, nullable=False)
    name = db.Column("name", db.String(100), nullable=False)
    sex = db.Column("sex", db.String(50), nullable=False)
    color = db.Column("color", db.String(100), nullable=False)
    date_of_birth = db.Column("date_of_birth", db.String(100), nullable=False)
    image_url = db.Column("image_url", db.String(200), nullable=False)


@dataclass
class PigeonHierarchy(db.Model):
    _id: int
    child_id: int
    father_id: int
    mother_id: int

    __tablename__ = "pigeon_hierarchy"
    _id = db.Column("id", db.Integer, primary_key=True)
    child_id = db.Column(
        "child_id",
        db.Integer,
        db.ForeignKey("pigeons.id", ondelete="CASCADE"),
        nullable=False,
    )
    father_id = db.Column(
        "father_id",
        db.Integer,
        db.ForeignKey("pigeons.id", ondelete="CASCADE"),
        nullable=False,
    )
    mother_id = db.Column(
        "mother_id",
        db.Integer,
        db.ForeignKey("pigeons.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "child_id", "father_id", "mother_id", name="unique_constraint"
        ),
    )
