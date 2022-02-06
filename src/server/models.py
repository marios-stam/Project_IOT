from flask_login import UserMixin  # Provides default implementations
from flask_sqlalchemy import SQLAlchemy
from . import db


class User(db.Model, UserMixin):
    """Data model for user accounts."""

    __tablename__ = 'Users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(64),
        index=False,
        unique=False,
        nullable=False
    )

    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    role = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
    )
    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Bin(db.Model):
    __tablename__ = 'Bins'
    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=False
    )

    status = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    fullness = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    longtitude = db.Column(
        db.Float,
        nullable=False
    )

    langtitude = db.Column(
        db.Float,
        nullable=False
    )

    updated = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return 'Bin with id:{} --->{} %'.format(self.id, self.fullness)


class Truck(db.Model):
    __tablename__ = 'Trucks'
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    status = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    fullness = db.Column(
        db.Integer,
        index=False,
        unique=False,
        nullable=False
    )

    position = db.Column(
        db.String(80),
        nullable=False
    )
    updated = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return "Truck:{} at position {} , {} full% ".format(self.username, self.position, self.fullnes)
