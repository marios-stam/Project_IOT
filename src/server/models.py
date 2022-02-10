from enum import unique
from multiprocessing import AuthenticationError
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

    points = db.Column(
        db.Integer,
        index=False,
        unique=False,
        default=0
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
    sensor_id = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    lat = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )

    long = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )

    fall_status = db.Column(
        db.Boolean,
        unique=False,
        nullable=True
    )

    battery = db.Column(
        db.Float,
        unique=False,
        nullable=True
    )

    time_online = db.Column(
        db.Integer,
        unique=False,
        nullable=False
    )

    entry_id = db.Column(
        db.Text,
        unique=True,
        nullable=False,
        primary_key=True
    )

    timestamp = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    fill_level = db.Column(
        db.Float,
        unique=False,
        nullable=True
    )

    temperature = db.Column(
        db.Float,
        unique=False,
        nullable=True
    )

    fire_status = db.Column(
        db.Boolean,
        unique=False,
        nullable=True
    )

    orientation = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )

    def __repr__(self):
        return 'Bin with id:{} --->{} %'.format(self.entry_id, self.fill_level)


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

    lat = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )

    long = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )
    updated = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return "Truck:{} at position [{},{}] , {} full% ".format(self.id, self.lat, self.long, self.fullness)


class Report(db.Model):
    __tablename__ = 'Reports'
    report_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        foreign_key='Users.id',
        nullable=False
    )

    details = db.Column(
        db.Text
    )

    status = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=False
    )

    updated = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return "Report:{} from user_id:{} ".format(self.report_id, self.user_id)
