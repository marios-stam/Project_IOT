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
        nullable=False,
        default=0
    )

    admin = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )

    reports = db.relationship('Report', backref='user', passive_deletes=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Bin(db.Model):
    __tablename__ = 'Bins'
    sensor_id = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    status = db.Column(
        db.Text,
        index=False,
        unique=False,
        nullable=True
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
        db.Text,
        primary_key=True
    )

    status = db.Column(
        db.Text,
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
        db.ForeignKey('Users.id', ondelete="CASCADE"),
        nullable=False
    )

    details = db.Column(
        db.Text,
        nullable=False
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


class Regression(db.Model):
    __tablename__ = 'Regression'
    sensor_id = db.Column(
        db.Text,
        primary_key=True,
        unique=True,
        nullable=False
    )

    angle = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )

    timestamp = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    def __repr__(self):
        return "Predicted angle:{} from sensor_id:{} ".format(self.angle, self.sensor_id)


class Bounty(db.Model):
    __tablename__ = 'Bounty'
    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True
    )

    long = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )

    lat = db.Column(
        db.Float,
        unique=False,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        unique=False,
        nullable=False
    )

    bin_id = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )

    message = db.Column(
        db.Text,
        unique=False,
        nullable=False,
        default="Lorem ipsum dolor sit amet"
    )

    points = db.Column(
        db.Integer,
        unique=False,
        nullable=False,
        default=0
    )

    type = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )

    assigned_usr_id = db.Column(
        db.Integer,
        unique=False,
        nullable=True
    )

    time_assigned = db.Column(
        db.DateTime,
        unique=False,
        nullable=True
    )

    completed = db.Column(
        db.Boolean,
        unique=False,
        nullable=False,
        default=False
    )

    def __repr__(self):
        return "Bounty for bin {}: {}".format(self.bin_id, self.message)
