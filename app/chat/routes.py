from app import db, socketio
from app.chat import bp
from app.models import User, Room, Message
from app.chat.forms import ChatForm
from werkzeug.urls import url_parse
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from flask_socketio import join_room, leave_room, send, emit


@bp.route('/room/<name>', methods=['GET', 'POST'])
@login_required
def room(name):
    room = Room.query.filter_by(name=name).first_or_404()
    avatar_url = current_user.get_avatar(50)
    return render_template('chat/room.html',
                           user=current_user,
                           username=current_user.username,
                           user_id=current_user.id,
                           avatar_url=avatar_url,
                           room=room,
                           roomname=room.name,
                           room_id=room.id,
                           messages=room.messages)


@socketio.on('user_message')
def user_message(data):
    room = data['room_id']
    message = Message(msg=data['msg'],
                      user_id=data['user_id'],
                      room_id=data['room_id'],
                      avatar=data['avatar_url'],
                      username=data['username'])
    db.session.add(message)
    db.session.commit()
    send({"msg": message.msg,
          "username": message.username,
          "timestamp": str(message.timestamp),
          "avatar_url": message.avatar}, room=room)


@socketio.on('join')
def on_join(data):
    room = data["room_id"]
    print(current_user, "joined room", room)
    join_room(room)


@socketio.on('leave')
def on_leave(data):
    room = data["room_id"]
    print(current_user, "left room", room)
    leave_room(room)
