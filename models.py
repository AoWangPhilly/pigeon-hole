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