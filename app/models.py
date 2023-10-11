from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db

from sqlalchemy import String, ForeignKey, Boolean, func
from sqlalchemy.orm import Mapped, Table, Column, mapped_column, relationship
from db import Model


UserRoom = Table(
    'UserRoom',
    Model.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True, nullable=False),
    Column('room_id', ForeignKey('room.id'), primary_key=True, nullable=False)
)


class Message(db.Model):
    __tablename__ = 'message'
    id: Mapped[int] = mapped_column(primary_key=True)
    msg: Mapped[str] = mapped_column(db.String(1000))
    timestamp: Mapped[datetime] = mapped_column(insert_default=func.now())
    username: Mapped[str] = mapped_column(String(150))
    avatar: Mapped[str] = mapped_column(String(150))
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'))
    room_id: Mapped[int] = mapped_column(
        ForeignKey('room.id'))

    def __repr__(self):
        return f'Message({self.username}, "{self.msg}")'

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
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True)
    username: Mapped[str] = mapped_column(String(150), index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(String(150))
    messages: Mapped['Message'] = relationship(
        backpopulates='user', lazy='dynamic')
    rooms: Mapped[list['Room']] = relationship(
        secondary=UserRoom,
        back_populates='users')
    about_me: Mapped[str] = mapped_column(String(140))
    last_seen: Mapped[str] = mapped_column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'User({self.username})'

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
        return self.rooms.where(UserRoom.room_id == self.room.id).count() > 0

    def joined_rooms(self):
        joined = Room.query.join(
            UserRoom,
            (UserRoom.c.room_id == Room.id)).filter(UserRoom.c.user_id == self.id)
        return joined

    def get_profile(self):
        return '/user/' + self.username

    def invitable_rooms(self, other_user):
        other_user_rooms = Room.query.join(
            UserRoom,
            (UserRoom.c.room_id == Room.id)).filter(UserRoom.c.user_id == other_user.id)
        own_user_rooms = Room.query.join(
            UserRoom,
            (UserRoom.c.room_id == Room.id)).filter(UserRoom.c.user_id == self.id)
        result = own_user_rooms.except_(other_user_rooms)
        return result

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Room(db.Model):
    __tablename__ = 'room'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True)
    private: Mapped[bool] = mapped_column(Boolean)
    users: Mapped[list['User']] = relationship(
        secondary=UserRoom,
        back_populates='rooms')
    messages: Mapped['Message'] = relationship(
        backpopulates='room', lazy='dynamic')

    def __repr__(self):
        return f'Room({self.name})'

    def __init__(self, name, private):
        self.name = name
        self.private = private
