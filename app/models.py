from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import login, db


user_room = db.Table('user_room',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
                     )


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    msg = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String(150))
    avatar = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return '<Message from %r in %r>' % self.user_id % self.room_id

    def __init__(self, msg, user_id, room_id, username, avatar):
        self.msg = msg
        self.user_id = user_id
        self.room_id = room_id
        self.username = username
        self.avatar = self.get_avatar(user_id)

    def get_avatar(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        return user.get_avatar(50)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    messages = db.relationship('Message', backref='user', lazy='dynamic')
    rooms = db.relationship('Room',
                            secondary=user_room,
                            backref=db.backref('user', lazy='dynamic'),
                            lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

    def get_avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __init__(self, email, username):
        self.email = email
        self.username = username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def join(self, room):
        if not self.has_joined(room):
            self.rooms.append(room)

    def leave(self, room):
        if self.has_joined(room):
            self.rooms.remove(room)

    def has_joined(self, room):
        return self.rooms.filter(user_room.c.room_id == room.id).count() > 0

    def joined_rooms(self):
        joined = Room.query.join(
            user_room,
            (user_room.c.room_id == Room.id)).filter(user_room.c.user_id == self.id)
        return joined

    def get_profile(self):
        return '/user/' + self.username

    def invitable_rooms(self, other_user):
        other_user_rooms = Room.query.join(
            user_room,
            (user_room.c.room_id == Room.id)).filter(user_room.c.user_id == other_user.id)
        own_user_rooms = Room.query.join(
            user_room,
            (user_room.c.room_id == Room.id)).filter(user_room.c.user_id == self.id)
        result = own_user_rooms.except_(other_user_rooms)
        return result

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    private = db.Column(db.Boolean, nullable=False)
    messages = db.relationship('Message', backref='room', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return '<Room %r>' % self.name

    def __init__(self, name, private, owner_id=None):
        self.name = name
        self.private = private
        self.owner_id = owner_id
