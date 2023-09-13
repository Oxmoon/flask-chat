from datetime import datetime
from . import db
from app import login
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


user_room = db.Table('user_room',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
                     )


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return '<Message from %r in %r>' % self.user_id % self.room_id


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    username = db.Column(db.String(150))
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    rooms = db.relationship('Room',
                            secondary=user_room,
                            backref=db.backref('user', lazy='dynamic'),
                            lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    messages = db.relationship('Message', backref='room', lazy='dynamic')

    def __repr__(self):
        return '<Room %r>' % self.name
