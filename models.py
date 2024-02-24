from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

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
    __tablename__ = "pigeons"
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), nullable=False)
    color = db.Column("color", db.String(100), nullable=False)
    birthday = db.Column("birthday", db.String(100), nullable=False)
    sex = db.Column("sex", db.Boolean, nullable=False)

# @dataclass
# class PigeonHierarchy(db.Model):
#     __tablename__ = "pigeon_hierarchy"
